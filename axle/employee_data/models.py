from django.db import models

# Create your models here.


class Employee(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email_address = models.EmailField(blank=False, null=False, unique=True)

