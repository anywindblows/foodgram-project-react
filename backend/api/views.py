from django_filters import rest_framework as drf_filter
from rest_framework import viewsets
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import RecipeFilter
from .models import Ingredient, Recipe, Tag, Favorite
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class TagsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = (drf_filter.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)
