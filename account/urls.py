from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('email-verification/<str:uidb64>/<str:token>', 
        views.EmailVerificationView.as_view(), 
        name='email-verification'
        ),
    path('email-verification-sent', 
         views.EmailVerificationSentView.as_view(), 
         name='email-verification-sent'
         ),
    path('email-verification-fail', 
         views.EmailVerificationFailView.as_view(), 
         name='email-verification-fail'
         ),
    path('email-verified', views.EmailVerifiedView.as_view(), name='email-verified'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.CustomLogoutView.as_view(), name='logout'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('delete', views.DeleteAccountView.as_view(), name='delete'),
    path('settings', views.SettingsView.as_view(), name='settings'),
    path('password-reset',
        auth_views.PasswordResetView.as_view(
            template_name="account/password/password-reset.html"
        ), 
        name='password-reset'), # allows users to submit an email form
    path('password-reset-sent', 
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password/password-reset-sent.html"
        ), 
        name='password_reset_done'), # success message routing for password reset sent
    path('reset/<uidb64>/<token>', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password/password-reset-form.html"
     ), 
     name='password_reset_confirm'),

    path('password-reset-complete', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password/password-reset-complete.html"
        ), 
        name='password_reset_complete')
]
