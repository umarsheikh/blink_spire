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
        parent_post = self.validated_data.get('parent_post')
        published_at = self.validated_data.get('published_at')

        if parent_post and published_at:
            try:
                parent_post_instance = Post.objects.get(pk=parent_post.id)
            except Post.DoesNotExist:
                raise serializers.ValidationError('Parent post does not exist.')

            if parent_post_instance.published_at and parent_post_instance.published_at > published_at:
                raise serializers.ValidationError('Post cannot be published before its parent post.')

        title = self.validated_data['title']
        tagline = self.validated_data['tagline']
        slug = slugify(title)
        meta_title = f'{title} - {tagline}' 

        return Post.objects.create(slug=slug, meta_title=meta_title, **self.validated_data)

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
            'published_at',
            'created_at'
        ]

class UpdatePostSerializer(serializers.ModelSerializer):
    parent_post_id = serializers.IntegerField()

    def validate_published_at(self, published_at):
        parent_post = self.instance.parent_post
        if published_at and parent_post and parent_post.published_at and parent_post.published_at > published_at:
            raise serializers.ValidationError('Post cannot be published before its parent post.')
        return published_at
    
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