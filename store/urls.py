from django.urls import path 
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('shop/', views.ShopIndexView.as_view(), name='store'),
    path('shop/<slug:slug>/', views.CategoriesView.as_view(), name='categories'),
    path('shop/<slug:slug>/', views.ProductInfoView.as_view(), name='product'),
]