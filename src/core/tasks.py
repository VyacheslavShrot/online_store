import requests

from celery import shared_task
from core.services.emails import send_report_email, send_client_report_email, send_admin_notification


@shared_task
def send_report_email_task(email, description):
    send_report_email(email=email, description=description)
    send_client_report_email(email=email, description=description)


@shared_task
def monitor_website():
    url = "http://localhost/"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            send_admin_notification(notification="Website is down!")
    except requests.RequestException as e:
        send_admin_notification(notification=f"Error: {str(e)}")
