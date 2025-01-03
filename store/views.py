from typing import Any
from django.shortcuts import redirect, get_object_or_404
from . models import Category, Product
from django.views.generic import TemplateView, ListView, DetailView



class StoreIndexView(TemplateView):
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['categories'] = Category.objects.all() 
        return context 

class HomePageView(TemplateView):
    template_name = "store/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

class CategoryProductsView(ListView):
    template_name = 'store/categories.html'  # Create this template
    model = Product
    context_object_name = 'products'

    def get(self, request, *args, **kwargs):
        if kwargs.get('slug') == 'all-products':
            return redirect('store')  # Redirect to home page

        return super().get(request, *args, **kwargs)  # Proceed with 

    def get_queryset(self):
        # Get the slug from the URL and filter products by category
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        return Product.objects.filter(category=category)
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Include categories in context for navigation
        context['selected_category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        return context


class ProductInfoView(DetailView):
    model = Product
    template_name = 'store/single-product.html'
    context_object_name = 'product'