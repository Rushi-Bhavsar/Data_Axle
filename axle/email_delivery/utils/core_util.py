from datetime import date
from dateutil.relativedelta import relativedelta
from employee_data.models import EmployeeEvents
from email_delivery.models import EmailTemplate


def calculate_date_difference(from_date, to_data):
    delta = relativedelta(from_date, to_data)
    years, months, days = delta.years, delta.months, delta.days
    if years > 0 and months == 0 and days == 0:
        return True, years
    else:
        return False, years


def add_number_suffix(number):
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
    return f"{number}{suffix}"


def process_template(data):
    email_payload = {'to_email': data['employee_info'].email_address, 'Email_Subject': '', 'Email_Body': ''}
    employee_full_name = f"{data['employee_info'].first_name} {data['employee_info'].last_name}"
    template = data['template']
    template = template.replace('{employee_name}', employee_full_name)
    year = add_number_suffix(str(data['year']))
    template = template.replace('{year}', year)
    subject = f"Happy {data['event_type']}"
    email_payload['Email_Body'] = template
    email_payload['Email_Subject'] = subject
    return email_payload


def create_template_data(employee_event_query, today_date):
    template_data = EmailTemplate.get_template_data()
    payload = []
    for event in employee_event_query:
        event_date = event.event_date
        event_type = event.event_type
        flag, year = calculate_date_difference(today_date, event_date)
        if flag and year:
            data = template_data.get(event_type, None)
            d = {'employee_info': event.employee, 'year': year, 'template': data, 'event_type': event_type}
            payload_details = process_template(d)
            payload_details['employee_event'] = event
            payload.append(payload_details)
    return payload
