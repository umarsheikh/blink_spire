from django.utils.text import slugify
from django.db.models import Value
from django.db.models.functions import Concat
from .base import *

class PostSerializer(serializers.ModelSerializer):
    parent_post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Post
        fields = [
            'id',
            'parent_post_id',
            'author',
            'title',
            'tagline',
            'summary',
            'content',
            'published',
            'published_at',
            'child_posts',
            'created_at'
        ]
        read_only_fields = [ 'published', 'child_posts', 'auther' ]

class CreatePostSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        title = self.validated_data['title']
        tagline = self.validated_data['tagline']
        slug = slugify(title)
        meta_title = f'{title} - {tagline}' 
        return Post.objects.create(slug=slug, meta_title=meta_title, **self.validated_data )

    class Meta:
        model = Post
        fields = [
            'id',
            'parent_post',
            'author',
            'title',
            'tagline',
            'summary',
            'content',
            'published',
            'published_at',
            'created_at'
        ]
        read_only_fields = [ 'published' ]

class UpdatePostSerializer(serializers.ModelSerializer):
    parent_post_id = serializers.IntegerField()
    
    def validate_parent_post_id(self, id):
        if not Post.objects.filter(pk = id).exists():
            raise serializers.ValidationError('Product with this ID does not exists')
        if id == self.instance.id:
            raise serializers.ValidationError("Parent post cannot be the same as the post itself.")
        return id

    def save(self, **kwargs):
        title = self.validated_data['title']
        tagline = self.validated_data['tagline']
        slug = slugify(title)
        meta_title = f'{title} - {tagline}'
        return Post.objects.update(slug=slug, meta_title=meta_title, **self.validated_data )

    class Meta:
        model = Post
        fields = [
            'parent_post_id',
            'author',
            'title',
            'tagline',
            'summary',
            'content',
            'published_at',
        ]