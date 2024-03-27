from .base import *
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField()
    summary = models.CharField(max_length=255)
    content = models.TextField()
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True, validators=[DateTimeValidator(future=True)])

    parent_post = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='child_posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.title} - {self.author.username}'