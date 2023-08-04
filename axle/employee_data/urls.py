from django.urls import path
from .user_view import UserDetailAPI, RegisterUserAPIView

urlpatterns = [
    path("get-details/", UserDetailAPI.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
]
