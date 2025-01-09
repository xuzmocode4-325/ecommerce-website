from django.urls import path
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
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('delete', views.DeleteAccountView.as_view(), name='delete'),
    path('settings', views.SettingsView.as_view(), name='settings'),
]
