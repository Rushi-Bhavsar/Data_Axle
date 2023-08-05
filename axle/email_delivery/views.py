from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import EmailTemplate
from employee_data.models import EmployeeEvents


class TriggerEmail(APIView):

    def get(self, request):
        today_date = timezone.now()

        pass
