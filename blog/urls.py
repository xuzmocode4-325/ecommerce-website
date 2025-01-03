from django.urls import path
from . import views

urlpatterns = [
    path("blog/", views.BlogHomeView.as_view(), name="blog"), 
    path("blog/posts/", views.BlogPostsView.as_view(), name="all-posts"),
    path("blog/posts/<slug:slug>", views.BlogDetailView.as_view(), name="single-post-page"),
    path("blog/posts/read-later", views.ReadLaterView.as_view(), name="read-later")
]