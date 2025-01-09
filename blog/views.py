from typing import Any
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Topic
from .forms import CommentForm

# Create your views here

class BlogIndexView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        context['posts'] = Post.objects.all().order_by('-created_at')[:9]
        return context

class BlogTopicsView(ListView):
    template_name = 'blog/index.html'  # Create this template
    model = Post
    context_object_name = 'posts'

    def get(self, request, *args, **kwargs):
        if kwargs.get('slug') == 'all-posts':
            return redirect('blog')  # Redirect to home page

        return super().get(request, *args, **kwargs)  # Proceed with 

    def get_queryset(self):
        # Get the slug from the URL and filter products by Topic
        slug = self.kwargs['slug']
        topic = get_object_or_404(Topic, slug=slug)
        return Post.objects.filter(topic=topic)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()  # Include categories in context for navigation
        context['selected_topic'] = get_object_or_404(Topic, slug=self.kwargs['slug'])
        return context


class BlogDetailView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None: 
            saved_for_read_later = post_id in stored_posts
        else:
            saved_for_read_later = False
        return saved_for_read_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
       
        post_comments = post.post_comments.all().order_by("-created_at") 
        context = {
            "post": post,
            "post_tags": post.tag.all(),
            "comment_form": CommentForm(),
            "post_comments": post_comments,
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        print(post_comments)
        return render(
            request, 
            "blog/single-post.html",
            context
        )

    def post(self, request, slug): 
        """
        Handles the submission of a comment for a specific blog post.

        This method retrieves the blog post identified by the given slug,
        processes the submitted comment form, and saves the comment if valid.
        It also captures the user's IP address and associates it with the comment.

        Args:
            request: The HTTP request object containing the submitted data.
            slug (str): The slug of the blog post to which the comment is being added.

        Returns:
            HttpResponseRedirect: Redirects to the single post page if the comment is successfully saved.
            render: Renders the single post page with the post details and an empty comment form if the form is invalid.
        """
        post = get_object_or_404(Post, slug=slug)
        authenticated = request.user.is_authenticated
        user = request.user
        ip_address = request.META.get('REMOTE_ADDR')
        comment_form = (
            CommentForm(request.POST)
        )
        post_comments = post.post_comments.all().order_by("-created_at")
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = user if authenticated else None
            comment.ip_adress = ip_address
            comment.save()
            return HttpResponseRedirect(
                reverse("single-post-page",
                    args=[slug]
                )
            )
        context = {
            "post": post,
            "post_tags": post.tag.all(),
            "comment_form": CommentForm(),
            "post_comments": post_comments,
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        print(post_comments)
        return render(
            request, 
            "blog/single-post.html",
            context
        )

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else: 
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request, "blog/stored-posts.html", context)
    
    def post(self, request):
        stored_posts = request.session.get("stored_posts")
        post_id = int(request.POST["post_id"])

        if stored_posts is None:
            stored_posts = []
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")