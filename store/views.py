from typing import Any
from django.shortcuts import redirect
from . models import Category, Product
from django.views.generic import TemplateView, ListView, DetailView



class ShopIndexView(TemplateView):
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['categories'] = Category.objects.all() 
        #print(context['categories'])
        return context 

class HomePageView(TemplateView):
    template_name = "store/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


# class CategoriesView(ListView):
#     template_name = "store/categories.html"
#     model = Category
#     context_object_name = 'category'
#     queryset = Category.objects.all()

#     def get(self, request, *args, **kwargs):
#         if kwargs.get('slug') == 'all-products':
#             return redirect('store')  # Redirect to home page

#         return super().get(request, *args, **kwargs)  # Proceed with 

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
        return Product.objects.filter(category__slug=slug)  # Assuming Product has a ForeignKey to Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Include categories in context for navigation
        context['selected_category'] = Category.objects.get(slug=self.kwargs['slug'])  # Get the selected category
        return context


class ProductInfoView(DetailView):
    model = Product
    template_name = 'store/single-product.html'
    context_object_name = 'product'