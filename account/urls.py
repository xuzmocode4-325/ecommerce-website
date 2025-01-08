from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('email-verification/<str:uidb64>/<str:token>', views.EmailVerificationView.as_view(), name='email-verification'),
    path('email-verification-sent', views.EmailVerificationSentView.as_view(), name='email-verification-sent'),
    path('email-verification-fail', views.EmailVerificationFailView.as_view(), name='email-verification-fail'),
    path('email-verified', views.EmailVerifiedView.as_view(), name='email-verified'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard')
]
