from typing import Union

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.serializers import FollowSerializer
from api.v1.pagination import LimitPageNumberPagination
from config import config_messages as msg
from services.user_services import UserServices

from .models import Follow

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    http_method_names = ['get', 'post', 'delete']
    pagination_class = LimitPageNumberPagination

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request: Request, id: int = None
                  ) -> Union[Response, None]:
        """Create or delete subscribe relations between users."""
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            error_validate = UserServices().validate_post_method(author, user)
            if error_validate:
                return Response(
                    error_validate,
                    status=status.HTTP_400_BAD_REQUEST
                )

            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(follow, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            error_validate = UserServices().validate_delete_method(
                author, user)
            if error_validate:
                return Response(
                    error_validate,
                    status=status.HTTP_400_BAD_REQUEST
                )
            follow = Follow.objects.filter(user=user, author=author)
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(
                {'errors': msg.ALREADY_UNSIGNED},
                status=status.HTTP_400_BAD_REQUEST
            )
        return None

    @action(
        detail=False, methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request: Request) -> Response:
        user = request.user
        queryset = Follow.objects.filter(user=user)
        paginate = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            paginate,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
