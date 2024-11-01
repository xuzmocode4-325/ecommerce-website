from django.views.generic import TemplateView

# Create your views here.

class ShopIndexView(TemplateView):
    template_name = 'shop/index.html'