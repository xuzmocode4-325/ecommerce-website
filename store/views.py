from typing import Any
from . models import Category
from django.views.generic import TemplateView, ListView, DetailView



class ShopIndexView(TemplateView):
    template_name = 'store/store.html'

class HomePageView(TemplateView):
    template_name = "store/home.html"


class CategoriesView(ListView):
    template_name = "store/categories.html"
    model = Category
    context_object_name = 'categories'
    queryset = Category.objects.all()


class ProductInfoView(DetailView):
    template_name = 'store/product.html'