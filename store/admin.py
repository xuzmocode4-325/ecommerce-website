from django.contrib import admin
from .models import Category, Product, Tag

# # Register your models here.

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('tag',)}
    pass

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    pass

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    pass

admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)