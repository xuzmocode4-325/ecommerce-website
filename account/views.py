from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.

class UserRegisterView(TemplateView):
    template_name = 'account/registration/register.html'