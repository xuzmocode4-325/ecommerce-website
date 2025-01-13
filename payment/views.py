from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView

from django_countries import countries

from . models import ShippingAddress, Order, OrderItem
from cart.cart import Cart

# Create your views here.

class PaymentSuccessView(TemplateView):
    template_name = 'payment/payment-success.html'


class PaymentFailView(TemplateView):
    template_name = 'payment/payment-fail.html'


class CheckoutView(TemplateView):
    template_name = 'payment/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country_choices = list(countries)
        context['countries'] = country_choices
        if self.request.user.is_authenticated:
            try:
                context['shipping'] = ShippingAddress.objects.get(
                    user=self.request.user.id
                )
                return context
            except:
                return context
        return context
    
class CompleteOrderView(FormView):
    template_name = 'complete-order.html'  # Your template file
    success_url = reverse_lazy('order_success')  # Redirect after successful submission

    def get(self, request, *args, **kwargs):
        # Render the template for GET requests
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Manually handle POST data without using a form class
        firstname = request.POST.get('firstname')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zipcode = request.POST.get('zipcode')

        full_name = f'{firstname} {surname}'

        # Order address 
        shipping_address = (
            address1 + "\n" + address2 + "\n" 
            + city + "\n" + state + "\n" + country + "\n"
            + zipcode
        )

        # Cart info
        cart = Cart(request)
        total_cost = cart.get_total()

        if request.user.is_authenticated:
            order = Order.objects.create(
                full_name=full_name, 
                email=email, 
                shipping_address=shipping_address,
                amount_paid=total_cost,
                user=request.user
            )

            order_id = order.pk

            for item in cart: 
                OrderItem.objects.create(
                    order_id=order_id, 
                    product=item['product'], 
                    quantity=item['qty'], 
                    price=item['price'], 
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
                )
        order_success = True
            
        # Return a JSON response or redirect as needed
        return JsonResponse({'success':order_success})