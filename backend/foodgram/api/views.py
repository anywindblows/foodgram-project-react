from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

from users.models import User


class APIUsersView(APIView):
    """Returns a list of users, or creates a new one."""

    def get(self, request: Request, user_id: int = None) -> Response:
        try:
            users = User.objects.filter(id=user_id)
        except ValueError:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIUsersMeView(APIView):
    def get(self, request):
        pass
