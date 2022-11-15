from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet

from .views import IngredientsViewSet, RecipesViewSet, TagsViewSet

app_name = 'api'

router = DefaultRouter()
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipesViewSet)
router.register('tags', TagsViewSet)
router.register('users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
