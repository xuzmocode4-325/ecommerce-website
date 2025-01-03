from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from store.models import Tag
# Create your models here.

class Author(models.Model):
    pass

class Topic(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=130, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Post(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/posts", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True
    )
    content = models.TextField(validators=[MinLengthValidator(255)])
    author = models.ForeignKey(
        Author, related_name='posts', on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        related_name='post_comments', 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, 
        related_name='user_comments', 
        on_delete=models.CASCADE,
        null=True
    )
    published = models.BooleanField(default=False)
    comment = models.TextField(max_length=450)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True)

    @property
    def display_user(self):
        return self.user.username if self.user else "Anon"


    def __str__(self):
        return f"{self.user} on {self.post}"
    
