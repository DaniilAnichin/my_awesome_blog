from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .permissions import IsAuthor
from .models import Post
from .serializers import AuthorSerializer, PostSerializer

User = get_user_model()


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthor]
    filter_fields = ('views', 'author__name', 'title', 'tags', 'created_at')
    search_fields = ('title', 'body', 'tags__name')
    ordering_fields = ('title', 'body', 'created_at', 'views')

    def get_object(self):
        instance = super().get_object()
        instance.increment_views()
        return instance


class AuthorViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthorSerializer
