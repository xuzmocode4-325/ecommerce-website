from django.urls import path 
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='store'),
    path('categories/<slug:slug>/', views.CategoriesView.as_view(), name='categories'),
]