from typing import Union

from django.http import FileResponse
from django_filters import rest_framework as drf_filter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.utils.filters import IngredientSearchFilter, RecipeFilter
from api.utils.pagination import LimitPageNumberPagination
from api.utils.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from services.api_services import (add_obj, create_buy_list, create_pdf_file,
                                   delete_obj)

from .models import Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShortRecipeSerializer, TagSerializer)


class TagsViewSet(ReadOnlyModelViewSet):
    """Tag view set."""
    http_method_names = ['get']
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Ingredients view set."""
    http_method_names = ['get']
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipesViewSet(viewsets.ModelViewSet):
    """Recipes view set."""
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = LimitPageNumberPagination
    filter_backends = (drf_filter.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer) -> None:
        """
        Specifies the behavior of the need to match author and request.user.
        """
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(
            self, request: Request, pk: int = None
    ) -> Union[Response, None]:
        """
        Create or delete favorite-recipe relations
        or return None, if http method not allowed.
        """
        if request.method == 'POST':
            return add_obj(Favorite, ShortRecipeSerializer, request.user, pk)
        if request.method == 'DELETE':
            return delete_obj(Favorite, request.user, pk)
        return None

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(
            self, request: Request, pk: int = None
    ) -> Union[Response, None]:
        """
        Add or remove recipe from shopping cart
        or return None, if http method not allowed.
        """
        if request.method == 'POST':
            return add_obj(Cart, ShortRecipeSerializer, request.user, pk)
        if request.method == 'DELETE':
            return delete_obj(Cart, request.user, pk)
        return None

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request: Request) -> FileResponse:
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')

        buy_list = create_buy_list(ingredients)
        pdf_file = create_pdf_file(buy_list)
        return FileResponse(
            pdf_file, as_attachment=True, filename='buylist.pdf'
        )
