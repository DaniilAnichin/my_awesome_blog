from rest_framework.routers import DefaultRouter

from .views import PostViewset, AuthorViewset


app_name = 'blog'
router = DefaultRouter()
router.register('posts', PostViewset, base_name='post')
router.register('authors', AuthorViewset, base_name='author')
urlpatterns = router.urls
