from django.contrib import admin
from .models import Category, Product

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    pass

class ProductAdmin(admin.ModelAdmin):
    repopulated_fields = {'slug':('title',)}
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)