import json
from django.shortcuts import redirect, get_object_or_404
from .cart import Cart
from store.models import Product
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, DetailView

# Create your views here.

class CartSummaryView(TemplateView):
    template_name = 'cart/cart-index.html'
    
class CartAddView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)

        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Access the action, product_id, and product_qty from the parsed data
            if data.get('action') == 'post':
                product_id = int(data.get('product_id'))
                product_qty = int(data.get('product_quantity'))
                
                product = get_object_or_404(Product, id=product_id)
                cart.add(product=product, product_qty=product_qty)

                cart_qty = cart.__len__()

                response = JsonResponse({
                    'status': 'success',
                    'product_name': product.title,
                    'product_qty': product_qty,
                    'cart_qty': cart_qty
                })

                

                return response
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)
        
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            # Handle JSON parsing errors and invalid data types
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    


class CartDeleteView(TemplateView):
    template_name = 'cart/cart-index.html'


class CartUpdateView(TemplateView):
    template_name = 'cart/cart-index.html'