from django.urls import path
from .views import APIUsersView

app_name = 'api'

urlpatterns = [
    path('users/', APIUsersView.as_view()),
    path('users/<int:user_id>/', APIUsersView.as_view()),
    path('users/me/', APIUsersView.as_view()),
]
