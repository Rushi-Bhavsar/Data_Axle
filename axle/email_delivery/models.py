from django.db import models
from employee_data.models import EmployeeEvents


class EmailTemplate(models.Model):
    event_type = models.CharField(max_length=10, blank=False, null=False)
    event_template = models.TextField(blank=False, null=False)

    @classmethod
    def get_template_data(cls):
        template_data = cls.objects.all().values('event_type', 'event_template')
        template_dict = dict()
        for template in template_data:
            template_dict[template['event_type']] = template['event_template']
        return template_dict


class EmailStatusChoice(models.TextChoices):
    SUCCESS = 'S', 'SUCCESS'
    FAILURE = 'F', 'FAILURE'
    NO_EVENT = 'N', 'NO EVENT'


class EmployeeEventEmailHistory(models.Model):
    employee_event = models.ForeignKey(to=EmployeeEvents, on_delete=models.CASCADE, null=True, blank=True)
    email_subject = models.CharField(max_length=100, blank=True, null=True)
    email_body = models.TextField(blank=True, null=True)
    email_status = models.CharField(max_length=1, choices=EmailStatusChoice.choices)
    email_timestamp = models.DateTimeField(auto_now_add=True)
    email_failure_reason = models.TextField(blank=True, null=True)
    error_message = models.CharField(max_length=200, null=True, blank=True)

    @classmethod
    def get_employee_event_id_for_today(cls, today_date):
        return cls.objects.filter(email_timestamp__date=today_date, email_status='S').values_list('employee_event',
                                                                                                  flat=True).distinct()

    @classmethod
    def check_already_stamp(cls, today_date):
        return cls.objects.filter(email_status='N', email_timestamp__date=today_date)
