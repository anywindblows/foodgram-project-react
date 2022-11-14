from typing import Union

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import FollowSerializer
from api.utils.pagination import LimitPageNumberPagination

from .models import Follow

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request: Request, id: int = None) -> Union[
        Response, None
    ]:
        message = dict()
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if user == author:
                message['errors'] = (
                    'Невозможно оформить подписку на самого себя.'
                )
            elif Follow.objects.filter(user=user, author=author).exists():
                message['errors'] = 'Вы уже подписаны на данного пользователя.'

                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(follow, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if user == author:
                return Response(
                    {'errors': 'Вы не можете отписываться от самого себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            follow = Follow.objects.filter(user=user, author=author)
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(
                {'errors': 'Вы уже отписались'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return None

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request: Request) -> Response:
        user = request.user
        queryset = Follow.objects.filter(user=user)
        paginate_queryset = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            paginate_queryset,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
