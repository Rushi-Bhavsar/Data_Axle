from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .user_view import UserDetailAPI, RegisterUserAPIView
from . import views


router = DefaultRouter()
router.register('add_employee', viewset=views.EmployeeViewSet, basename='add_employee')
router.register('add_event', viewset=views.EmployeeEventsViewSet, basename='add_event')

urlpatterns = [
    path("get-details/", UserDetailAPI.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
    path('', include(router.urls))
]
