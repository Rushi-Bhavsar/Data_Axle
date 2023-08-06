# Generated by Django 4.2.4 on 2023-08-06 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_data', '0002_employeeevents_event_month'),
        ('email_delivery', '0002_employeeeventemailhistory_error_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeeventemailhistory',
            name='email_body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employeeeventemailhistory',
            name='email_subject',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employeeeventemailhistory',
            name='employee_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee_data.employeeevents'),
        ),
    ]
