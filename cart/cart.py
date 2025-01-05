import copy
from decimal import Decimal
from store.models import Product
from django.urls import reverse


class Cart():
    def __init__(self, request):
        self.session = request.session

        # obtain existing session from returning user
        cart = self.session.get('session_key')

        # generate a new session for new user
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart


    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())
    

    def __iter__(self):
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
        product_id = str(product.id)

        if product_id in self.cart: 
            self.cart[product_id]['qty'] = product_qty
        else:
            self.cart[product_id] = {
                'price': str(product.price),
                'qty': product_qty}
        self.session.modified = True


    def delete(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    
    def update(self, product_id, product_qty):
        product_id = str(product_id)
        product_qty = product_qty

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty

        self.session.modified = True

    
    def get_total(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

