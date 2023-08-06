from django.db import models
from django.utils import dates


class GenderChoices(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other'


class Employee(models.Model):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email_address = models.EmailField(blank=False, null=False, unique=True)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, default=GenderChoices.OTHER)

    def __str__(self):
        return str(self.email_address)


class EmployeeEvents(models.Model):
    employee = models.ForeignKey(to=Employee, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=10, blank=False, null=False)
    event_date = models.DateField(blank=False, null=False)
    event_month = models.IntegerField(choices=dates.MONTHS.items(), blank=True, null=True)

    class Meta:
        unique_together = ('employee', 'event_type')

    @classmethod
    def get_data_by_month(cls, month, email_sent_for_today_event_ids):
        return cls.objects.filter(event_month=month).exclude(pk__in=email_sent_for_today_event_ids)
