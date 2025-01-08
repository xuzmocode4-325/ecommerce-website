from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site

from . forms import CreateUserForm
from . helpers import send_email_with_fallback
from .token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

import logging

logger = logging.getLogger(__name__)

# Create your views here.


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
    pass

class EmailVerificationSentView(TemplateView):
    template_name = 'account/registration/email-verification-sent.html'
    pass

class EmailVerifiedView(TemplateView):
    template_name = 'account/registration/email-verified.html'
    pass