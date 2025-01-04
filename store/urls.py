from django.urls import path 
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('store/', views.StoreIndexView.as_view(), name='store'),
    path('store/product/<slug:slug>/', views.ProductInfoView.as_view(), name='product-info'),
    path('store/category/<slug:slug>/', views.CategoryProductsView.as_view(), name='categories'),
]