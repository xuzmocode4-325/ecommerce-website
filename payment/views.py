from django.views.generic import TemplateView
from . models import ShippingAddress

# Create your views here.

class PaymentSuccessView(TemplateView):
    template_name = 'payment/payment-success.html'


class PaymentFailView(TemplateView):
    template_name = 'payment/payment-fail.html'


class CheckoutView(TemplateView):
    template_name = 'payment/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['shipping'] = ShippingAddress.objects.get(
                    user=self.request.user.id
                )
                return context
            except:
                return context
        return context