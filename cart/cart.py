import copy
from decimal import Decimal
from store.models import Product
from django.urls import reverse

from cart.models import Coupon

class Cart():
    def __init__(self, request):
        """
        Initialize the cart with the session data from the request.
        If the session does not have a cart, create a new empty cart.
        
        :param request: The HTTP request object containing session data.
        """
        self.session = request.session

        # obtain existing session from returning user
        cart = self.session.get('session_key')

        # generate a new session for new user
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

        # Initialize coupon
        self.coupon = self.session.get('coupon', None)

    def __len__(self):
        """
        Return the total number of items in the cart.
        
        :return: Total quantity of all items in the cart.
        """
        return sum(item['qty'] for item in self.cart.values())
    
    def __iter__(self):
        """
        Iterate over the items in the cart, adding product details and calculating totals.
        
        :yield: Each item in the cart with additional product information and total price.
        """
        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        cart = copy.deepcopy(self.cart)

        for product in products:
            cart[str(product.id)]['product'] = product
            cart[str(product.id)]['url'] = reverse('product-info', args=[product.slug])

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item

    def add(self, product, product_qty):
        """
        Add a product to the cart or update its quantity if it already exists.
        
        :param product: The product to add or update in the cart.
        :param product_qty: The quantity of the product to add or update.
        """
        product_id = str(product.id)

        if product_id in self.cart: 
            self.cart[product_id]['qty'] = product_qty
        else:
            self.cart[product_id] = {
                'price': str(product.price),
                'qty': product_qty}
        self.session.modified = True

    def delete(self, product_id):
        """
        Remove a product from the cart by its ID.
        
        :param product_id: The ID of the product to remove from the cart.
        """
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def update(self, product_id, product_qty):
        """
        Update the quantity of a product in the cart.
        
        :param product_id: The ID of the product to update.
        :param product_qty: The new quantity of the product.
        """
        product_id = str(product_id)
        product_qty = product_qty

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty

        self.session.modified = True

    def apply_coupon(self, coupon_code):
        """
        Apply a coupon to the cart.
        
        :param coupon_code: The code of the coupon to apply.
        """
        try:
            coupon = Coupon.objects.get(name=coupon_code)
            self.coupon = coupon.discount
            self.session['coupon'] = self.coupon
        except Coupon.DoesNotExist:
            self.coupon = None
            self.session['coupon'] = None
        self.session.modified = True

    def get_total(self):
        """
        Calculate the total cost of all items in the cart, applying any coupon discount.
        
        :return: The total price of all items in the cart after applying the discount.
        """
        total = sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
        if self.coupon:
            total -= total * Decimal(self.coupon)
        return total