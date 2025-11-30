import json
from django.shortcuts import render, get_object_or_404
from .utils.cart import Cart
from store.models import Product
from django.views import View
from django.http import JsonResponse

# Create your views here.

class CartSummaryView(View):
    template_name = 'cart/cart-index.html'
    def get(self, request, *args, **kwargs):
        cart = Cart(request)  # Initialize the cart using the request
        context = {
            'cart': cart,  # Pass the cart instance to the context
        }
        return render(request, self.template_name, context)

    
class CartAddView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)

        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Access the action, product_id, and product_qty from the parsed data
            if data.get('action') == 'post':
                product_id = int(data.get('product_id'))
                product_qty = int(data.get('product_qty'))
                
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
    


class CartDeleteView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)

        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Access the action, product_id, and product_qty from the parsed data
            if data.get('action') == 'post':
                product_id = int(data.get('product_id'))
                
                cart.delete(product_id=product_id)
                cart_qty = cart.__len__()
                cart_total = cart.get_total()

                response = JsonResponse({
                    'status': 'success',
                    'cart_total': cart_total,
                    'cart_qty': cart_qty
                })

                return response

            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)
        
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            # Handle JSON parsing errors and invalid data types
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    


class CartUpdateView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)

        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Access the action, product_id, and product_qty from the parsed data
            if data.get('action') == 'post':
                product_id = int(data.get('product_id'))
                product_qty = int(data.get('product_qty'))

                cart.update(product_id=product_id, product_qty=product_qty)

                cart_qty = cart.__len__()
                cart_total = cart.get_total() 

                response = JsonResponse({
                    'status': 'success',
                    'cart_total': cart_total,
                    'cart_qty': cart_qty
                })

                return response
        
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            # Handle JSON parsing errors and invalid data types
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class ApplyCouponView(View):
    """
    Class-based view to apply a coupon to the cart. It expects a POST request with a JSON body containing the coupon code.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to apply a coupon.
        
        :param request: The HTTP request object.
        :return: JsonResponse indicating success or failure and the new total if successful.
        """
        try:
            # Parse the JSON body to get the coupon code
            data = json.loads(request.body)
            coupon_code = data.get('coupon_code', '')

            # Initialize the cart and apply the coupon
            cart = Cart(request)
            cart.apply_coupon(coupon_code)

            # Calculate the new total after applying the coupon
            new_total = cart.get_total()

            # Check if the coupon was successfully applied
            if cart.coupon:
                return JsonResponse({'success': True, 'new_total': str(new_total)})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid coupon code.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})