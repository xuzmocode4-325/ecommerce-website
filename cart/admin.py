from django.contrib import admin

# Register your models here.
from .models import Coupon


class CouponAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'is_active')


admin.site.register(Coupon, CouponAdmin)