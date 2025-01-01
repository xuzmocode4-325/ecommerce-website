from typing import Any
from . models import Category, Product
from django.views.generic import TemplateView, ListView, DetailView



class ShopIndexView(TemplateView):
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context 

class HomePageView(TemplateView):
    template_name = "store/home.html"


class CategoriesView(ListView):
    template_name = "store/categories.html"
    model = Category
    context_object_name = 'categories'
    queryset = Category.objects.all()

class ProductInfoView(DetailView):
    model = Product
    template_name = 'store/single-product.html'
    context_object_name = 'product'