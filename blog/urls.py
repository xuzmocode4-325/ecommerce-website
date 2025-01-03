from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogIndexView.as_view(), name='blog'),
    path('<slug:slug>/', views.BlogTopicsView.as_view(), name='topics'),
]