
from django.urls import reverse_lazy
from django.shortcuts import render

from django.views.generic import TemplateView, FormView
from . forms import CreateUserForm
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
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

    def get_context_data(self, uidb64, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uid'] = force_str(urlsafe_base64_decode(uidb64))
        context['artwork'] = get_artwork('starfield')
        return context

    def form_valid(self, form):
        try:
            user = form.save()
            user.is_active = False
            user.save()

            # e-mail verification setup.

            current_site = get_current_site(self.request)
            subject = 'Account verification email'
            message = render_to_string(
                'account/registration/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_decode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user)  
            })

            user.email_user(subject=subject, message=message)

            logger.info('User saved successfully.')

            return super().form_valid(form)

        except Exception as e:
            logger.exception(f'An error occurred in form_valid: {e}')
            return render(self.request, 'index/error_500.html', status=500)
        
class EmailVerificationView(TemplateView):
    template_name = 'account/registration/email-verification.html'
    pass

class EmailVerificationFailView(TemplateView):
    template_name = 'account/registration/email-verification-fail.html'
    pass

class EmailVerificationSentView(TemplateView):
    template_name = 'account/registration/email-verification-sent.html'
    pass

class EmailVerifiedView(TemplateView):
    template_name = 'account/registration/email-verified.html'
    pass