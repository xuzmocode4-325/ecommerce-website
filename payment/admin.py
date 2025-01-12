from django.contrib import admin
from django.contrib.auth.models import User
from .models import ShippingAddress

# Register your models here.

class ShippingAddressAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Prepopulate the email field with the current user's email
        if request.user.is_authenticated:
            form.base_fields['email'].initial = request.user.email
        return form

admin.site.register(ShippingAddress, ShippingAddressAdmin)