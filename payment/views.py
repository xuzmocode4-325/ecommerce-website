import json
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView

from django_countries import countries

from . models import ShippingAddress, Order, OrderItem
from cart.cart import Cart

import logging
logger = logging.getLogger(__name__)

# Create your views here.

class PaymentSuccessView(TemplateView):
    template_name = 'payment/payment-success.html'

    def get_context_data(self, **kwargs):
        for key in list(self.request.session.keys()):
            if key == 'session_key':
                del self.request.session[key]
        return super().get_context_data(**kwargs)


class PaymentFailView(TemplateView):
    template_name = 'payment/payment-failed.html'


class CheckoutView(TemplateView):
    template_name = 'payment/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country_choices = list(countries)
        context['cart'] = Cart(self.request)  # Initialize the cart using the request
        context['countries'] = country_choices
        if self.request.user.is_authenticated:
            try:
                context['shipping'] = ShippingAddress.objects.get(
                    user=self.request.user.id
                )
                return context
            except:
                return context
        else:
            return context
    
class CompleteOrderView(FormView):
    success_url = reverse_lazy('payment-success')  # Redirect after successful submission

    def get(self, request, *args, **kwargs):
        # Render the template for GET requests
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
    # Manually handle POST data without using a form class
        try:
            data = json.loads(request.body)
            firstname = data.get('fn', '')
            surname = data.get('sn', '')
            email = data.get('em', '')
            address1 = data.get('ad1', '')
            address2 = data.get('ad2', '')
            city = data.get('ct', '')
            state = data.get('st', '')
            country = data.get('cntry', '')
            zipcode = data.get('zip', '')
        except json.JSONDecodeError:
            pass

        full_name = f'{firstname} {surname}'

        # Order address
        shipping_address = "\n".join(filter(None, [address1, address2, city, state, country, zipcode]))

        # Cart info
        cart = Cart(request)
        total_cost = cart.get_total()

        try:
            if request.user.is_authenticated:
                order = Order.objects.create(
                    full_name=full_name,
                    email=email,
                    shipping_address=shipping_address,
                    amount_paid=total_cost,
                    user=request.user
                )
            else:
                order = Order.objects.create(
                    full_name=full_name,
                    email=email,
                    shipping_address=shipping_address,
                    amount_paid=total_cost,
                )

            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price'],
                    user=request.user if request.user.is_authenticated else None
                )

            order_success = True
        except Exception as e:
            order_success = False
            # Log the exception or handle it as needed
            print(f"Error creating order: {e}")

        # Return a JSON response or redirect as needed
        return JsonResponse({'success': order_success})