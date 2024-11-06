from django.urls import path
from . import views
from store import views as storeviews

urlpatterns = [
    path('shop', views.ShopIndexView.as_view(), name='shop'),
]