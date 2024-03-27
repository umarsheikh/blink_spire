from rest_framework.viewsets import ModelViewSet
from .base import *

class PostViewSet(ModelViewSet):
    http_method_names =['get', 'post', 'patch', 'delete']

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePostSerializer
        if self.request.method == 'PATCH':
            return UpdatePostSerializer
        return PostSerializer