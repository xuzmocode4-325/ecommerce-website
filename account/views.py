from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView, FormView, View
from django.views.generic.edit import DeleteView

from django.contrib import messages
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
    form_class = LoginForm
    success_url = reverse_lazy('store')  # Redirect to the dashboard on successful login

    def form_valid(self, form):
        # Extract username and password from the form
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Authenticate the user
        user = authenticate(self.request, username=username, password=password)
        
        if user is not None:
            # Log the user in
            login(self.request, user)
            # Add a success message
            messages.success(self.request, 'You are now logged in.')
            return super().form_valid(form)  # Redirect to success_url
        else:
            # If authentication fails, add an error message
            messages.error(self.request, "Invalid username or password.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Add a generic error message for invalid form submissions
        messages.error(self.request, "There was an error with your login attempt.")
        return super().form_invalid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class DashboardView(TemplateView):
    template_name = 'account/dashboard/orders.html'

 
@method_decorator(login_required(login_url='login'), name='dispatch')
class CustomLogoutView(LogoutView):
    def get_context_data(self, **kwargs):
        """
        Preserves cart data during logout by clearing all session data except for the cart.
        """
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
        """
        Adds a success message upon logout and returns the URL to redirect to.
        """
        # Add a success message
        messages.success(self.request, 'You are now signed out.')
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
        messages.info(self.request, 'Account updated.')
        return super().form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class SettingsView(TemplateView):
    template_name = 'account/dashboard/settings.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'account/dashboard/delete-account.html'
    success_url = reverse_lazy('account-deleted')

    def get_queryset(self):
        # Ensure only the logged-in user can delete their own account
        return User.objects.filter(id=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        # Attempt to delete the user
        try:
            user = self.get_object()
            user.delete()  # Delete the user account
            logout(request)  # Log out the user after deletion
            messages.info(request, "Your account has been successfully deleted.")
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            messages.info(request, "There was an error deleting your account. Please try again.")
            return redirect('dashboard')  
        

class AccountDeletedView(TemplateView):
    template_name = 'account/dashboard/account-deleted.html'
