
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, FormView
from . forms import CreateUserForm
import logging

logger = logging.getLogger(__name__)

# Create your views here.

class UserRegisterView(FormView):
    template_name = 'account/registration/register.html'
    success_url = reverse_lazy('store')
    form_class = CreateUserForm

    def form_valid(self, form):
        try:
            form.save()
            logger.info('Form saved successfully.')

            return super().form_valid(form)

        except Exception as e:
            logger.exception(f'An error occurred in form_valid: {e}')
            return render(self.request, 'index/error_500.html', status=500)