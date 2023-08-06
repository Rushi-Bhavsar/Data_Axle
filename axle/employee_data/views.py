from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.response import Response

from email_delivery.utils.decorator_utils import CatchException
from .models import Employee, EmployeeEvents
from .serializers import EmployeeEventsSerializer, EmployeeSerializer


@method_decorator(CatchException, name='update')
@method_decorator(CatchException, name='list')
@method_decorator(CatchException, name='create')
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    http_method_names = ['get', 'post', 'patch']


@method_decorator(CatchException, name='update')
@method_decorator(CatchException, name='list')
@method_decorator(CatchException, name='create')
class EmployeeEventsViewSet(viewsets.ModelViewSet):
    queryset = EmployeeEvents.objects.all()
    serializer_class = EmployeeEventsSerializer
    http_method_names = ['get', 'post', 'patch']

    def create(self, request, *args, **kwargs):
        event_date = self.request.data['event_date']
        parsed_datetime = timezone.datetime.strptime(event_date, "%Y-%m-%d")
        event_date = parsed_datetime.date()
        event_month = event_date.month
        input_data = dict()
        for key in request.data:
            input_data[key] = request.data[key]
        input_data['event_month'] = event_month
        serializer = self.get_serializer(data=input_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

