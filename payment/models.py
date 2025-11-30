from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django_countries.fields import CountryField


class ShippingAddress(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300)
    city = models.CharField(max_length=255)
    #optional
    state = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True)
    country = CountryField(null=True, blank=True, blank_label="(Select Country)")
    #fk 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return 'Shipping Address - ' + str(self.pk)
    
class Order(models.Model): 
    full_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=10000)
    amount_papk = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Order - #' + str(self.pk)
    

class OrderItem(models.Model): 
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Order Items'
    
    def __str__(self):
        return 'Order Item - #' + str(self.pk)

