from typing import Any
from . models import Category
from django.views.generic import TemplateView, ListView

class HomePageView(TemplateView):
    template_name = "store/home.html"


class CategoriesView(ListView):
    template_name = "store/categories.html"
    model = Category
    context_object_name = 'categories'
    queryset = Category.objects.all()