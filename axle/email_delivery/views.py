from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.utils import timezone
from .models import EmployeeEventEmailHistory
from employee_data.models import EmployeeEvents
from .utils.core_util import create_template_data
from .utils.decorator_utils import CatchException


@method_decorator(CatchException, name='get')
class SendEventEmails(APIView):
    def get(self, request, *args, **kwargs):
        resp_dict = {}
        today_date = timezone.now().date()
        today_month = today_date.month
        email_sent_for_today_event_ids = EmployeeEventEmailHistory.get_employee_event_id_for_today(today_date)
        employee_event_query = EmployeeEvents.get_data_by_month(today_month, email_sent_for_today_event_ids)

        if not employee_event_query:
            # Log that no events are scheduled for the current period
            check_event_already_stamp = EmployeeEventEmailHistory.check_already_stamp(today_date)
            if not check_event_already_stamp:
                EmployeeEventEmailHistory.objects.create(email_status='N',
                                                         error_message='No events scheduled for today.')
            return JsonResponse({'message': 'No events scheduled for today.', 'result': []})
        email_payload = create_template_data(employee_event_query, today_date)
        if not email_payload:
            check_event_already_stamp = EmployeeEventEmailHistory.check_already_stamp(today_date)
            if not check_event_already_stamp:
                EmployeeEventEmailHistory.objects.create(email_status='N',
                                                         error_message='No events scheduled for today.')
            return JsonResponse({'message': 'No events scheduled for today.', 'result': []})
        for payload in email_payload:
            try:
                subject = payload['Email_Subject']
                to_email = payload['to_email']
                body = f"""{payload['Email_Body']}"""
                customer_event = payload['employee_event']
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[to_email],
                    fail_silently=False,
                )

                EmployeeEventEmailHistory.objects.create(employee_event=customer_event, email_status='S',
                                                         email_subject=subject, email_body=body)
                msg = 'Event emails sent successfully.'
                resp_dict[to_email] = msg
            except Exception as e:
                EmployeeEventEmailHistory.objects.create(employee_event=payload['employee_event'], email_status='F',
                                                         email_failure_reason=str(e),
                                                         email_subject=payload['Email_Subject'],
                                                         email_body=payload['Email_Body'])
                to_email = payload['to_email']
                msg = 'Error while sending email.'
                resp_dict[to_email] = msg
            continue
        return JsonResponse({'message': 'Email Summary', 'result': resp_dict})
