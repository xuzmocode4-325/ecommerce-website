from django.contrib import admin
from .models import ShippingAddress

# Register your models here.

class ShippingAddressAdmin(admin.ModelAdmin):
    pass

admin.site.register(ShippingAddress, ShippingAddressAdmin)