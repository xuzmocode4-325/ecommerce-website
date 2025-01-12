from django.views.generic import TemplateView

# Create your views here.

class PaymentSuccessView(TemplateView):
    template_name = 'payment/payment-success.html'


class PaymentFailView(TemplateView):
    template_name = 'payment/payment-fail.html'


class CheckoutView(TemplateView):
    template_name = 'payment/checkout.html'