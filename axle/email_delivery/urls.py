from django.urls import path
from . import views


urlpatterns = [
    path('trigger_email/', views.TriggerEmail.as_view())

]