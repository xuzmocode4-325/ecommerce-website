from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('email-verification', views.EmailVerificationView.as_view(), name='register'),
    path('email-verification-sent', views.EmailVerificationSentView.as_view(), name='register'),
    path('email-verification-fail', views.EmailVerificationFailView.as_view(), name='register'),
    path('email-verified', views.EmailVerifiedView.as_view(), name='register'),
]
