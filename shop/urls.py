from django.urls import path
from . import views

urlpatterns = [
    path('shop', views.ShopIndexView.as_view(), name='shop')
]