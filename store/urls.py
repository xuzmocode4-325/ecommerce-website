from django.urls import path 
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('store/', views.ShopIndexView.as_view(), name='store'),
    path('store/categories/<slug:slug>/', views.CategoriesView.as_view(), name='categories'),
    path('store/product/<slug:slug>/', views.ProductInfoView.as_view(), name='single-product'),
]