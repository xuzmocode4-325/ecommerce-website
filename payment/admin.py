from django.contrib import admin
from django.contrib.auth.models import User
from .models import ShippingAddress, Order, OrderItem

# Register your models here.

class ShippingAddressAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Prepopulate the email field with the current user's email
        if request.user.is_authenticated:
            form.base_fields['email'].initial = request.user.email
        return form
    
class OrderAdmin(admin.ModelAdmin):
    pass

class OrderItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)