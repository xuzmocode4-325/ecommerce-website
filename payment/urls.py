from django.urls import path
from . import views

urlpatterns = [
    path('payment-success', views.PaymentSuccessView.as_view(), name='payment-success'),
    path('payment-failed', views.PaymentFailView.as_view(), name='payment-failed'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('complete-order', views.CompleteOrderView.as_view(), name='complete-order')
]