from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView, FormView, View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site

from . forms import CreateUserForm, LoginForm, UpdateUserForm
from . helpers import send_email_with_fallback
from . token import user_tokenizer_generate


import logging

logger = logging.getLogger(__name__)

# Create your views here.

# Create a custom decorator for class-based views
def login_required_class(view):
    @method_decorator(login_required(login_url='login'))
    def wrapped_view(request, *args, **kwargs):
        return view(request, *args, **kwargs)
    return wrapped_view


class UserRegisterView(FormView):
    template_name = 'account/registration/register.html'
    success_url = reverse_lazy('email-verification-sent')
    form_class = CreateUserForm

    def form_valid(self, form):
        try:
            user = form.save()
            user.is_active = False

            print("Cleaned Data:", form.cleaned_data)

            # e-mail verification setup.

            current_site = get_current_site(self.request)
            user_email = [user.email]
            subject = 'Account verification email'
            message = render_to_string(
                'account/registration/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user)  
            })

            result = send_email_with_fallback(subject, message, user_email)
            logger.info(f'Email sending result: {result}')

            if not result:
                logger.error('Failed to send email. Rendering error page.')
                return render(self.request, 'account/error_500.html', status=500)
            else:
                user.save()
                logger.info('User saved successfully.')
            return super().form_valid(form)

        except Exception as e:
            logger.exception(f'An error occurred in form_valid: {e}')
            return render(self.request, 'account/error_500.html', status=500)


class EmailVerificationView(View):
    def get(self, request, *args, **kwargs):
        uid = kwargs.get('uidb64')
        token = kwargs.get('token')
        if uid is None or token is None:
            logger.error("UID is None, cannot retrieve user.")
            return render(self.request, 'account/error_500.html', status=500)
        
        try:
            # Decode the base64 encoded UID
            uid = urlsafe_base64_decode(uid).decode()
            # Convert the decoded UID to an integer
            uid = int(uid)
        except (TypeError, ValueError, OverflowError) as e:
            logger.error(f"Error decoding UID: {e}")
            return render(self.request, 'account/error_500.html', status=500)

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            logger.error(f"User with ID {uid} does not exist.")
            return render(self.request, 'account/error_500.html', status=500)
        
        try:
            # Decode the uidb64 to get the original user id
            if user and user_tokenizer_generate.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect('email-verified')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            return redirect('email-verification-fail')

     
class EmailVerificationFailView(TemplateView):
    template_name = 'account/registration/email-verification-fail.html'


class EmailVerificationSentView(TemplateView):
    template_name = 'account/registration/email-verification-sent.html'


class EmailVerifiedView(TemplateView):
    template_name = 'account/registration/email-verified.html'


class UserLoginView(FormView): 
    template_name = 'account/login.html'
    success_url = reverse_lazy('dashboard')
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Authenticate the user
        user = authenticate(self.request, username=username, password=password)
        
        if user is not None:
            # Log the user in
            login(self.request, user)
            return super().form_valid(form)  # Call to get_success_url will happen here
        else:
            # If authentication fails, add an error to the form
            form.add_error(None, "Invalid username or password.")
            return self.form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class DashboardView(TemplateView):
    template_name = 'account/dashboard/orders.html'

 
@method_decorator(login_required(login_url='login'), name='dispatch')
class CustomLogoutView(LogoutView):
    def get_context_data(self, **kwargs):
        try:
            # Preserve cart data
            cart_data = self.request.session.get('session_key', {})

            # Clear all session data except for the cart
            for key in list(self.request.session.keys()):
                if key == 'session_key':
                    continue
                else:
                    del self.request.session[key]

            # Restore cart data
            self.request.session['session_key'] = cart_data

        except KeyError:
            pass

        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('home')
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileView(FormView):
    template_name = 'account/dashboard/profile.html'
    success_url = reverse_lazy('dashboard')
    form_class = UpdateUserForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteAccountView(TemplateView):
    template_name = 'account/dashboard/delete.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
class SettingsView(TemplateView):
    template_name = 'account/dashboard/settings.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteAccountView(TemplateView):
    template_name = 'account/dashboard/delete.html' 

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        user.delete()
        return redirect('store')