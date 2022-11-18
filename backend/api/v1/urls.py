from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.v1.views import IngredientsViewSet, RecipesViewSet, TagsViewSet
from users.views import CustomUserViewSet

app_name = 'v1'

v1 = DefaultRouter()
v1.register('ingredients', IngredientsViewSet)
v1.register('recipes', RecipesViewSet)
v1.register('tags', TagsViewSet)
v1.register('users', CustomUserViewSet)

urlpatterns = [
    path('', include(v1.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
