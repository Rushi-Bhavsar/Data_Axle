from django.urls import path
from . import views


urlpatterns = [
    path('trigger_email/', views.SendEventEmails.as_view())

]