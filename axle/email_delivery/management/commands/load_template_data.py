from django.core.management.base import BaseCommand
from email_delivery.models import EmailTemplate


class Command(BaseCommand):
    help = 'Load new template Data'

    def handle(self, *args, **options):
        birthday_message = """<p>Happy Birthday, {employee_name}!</p>
<pre>
	Wishing you a fantastic {year} birthday filled with joy, laughter, and all the things you love.
	Have a wonderful day and a fantastic year ahead!
</pre>
<p>This is auto generated email, Please do not reply.</p>
<p>Best regards,<br>DataAxle Organization</p>"""
        work_anniversary = """<p>Hello {employee_name},</p>
<pre>
	Congratulations! We extend our best wishes to you on your work anniversary of service with the organization.
	You have successfully completed {year} in the organization.
</pre>
<p>This is auto generated email, Please do not reply.</p>
<p>Best regards,<br>DataAxle Organization</p>"""

        event_details = {'Birthday': birthday_message, 'WorkAnniversary': work_anniversary}
        for event in event_details:
            if not EmailTemplate.objects.filter(event_type=event).exists():
                EmailTemplate.objects.create(event_type=event, event_template=event_details[event])
            else:
                self.stdout.write(f"Event {event} already present in database.")
