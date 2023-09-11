from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_report_email(email, description):
    message = render_to_string(
        template_name="report_email.html",
        context={
            "email": email,
            "description": description,
        },
    )

    email_send = EmailMessage(subject="sle3pinghood", body=message, to=[settings.EMAIL_HOST_USER])
    email_send.content_subtype = "html"
    email_send.send(fail_silently=settings.EMAIL_FAIL_SILENTLY)


def send_client_report_email(email, description):
    message = render_to_string(
        template_name="client_report_email.html",
        context={
            "email": email,
            "description": description
        },
    )

    email_send = EmailMessage(subject="sle3pinghood", body=message, to=[email])
    email_send.content_subtype = "html"
    email_send.send(fail_silently=settings.EMAIL_FAIL_SILENTLY)


def send_admin_notification(notification):
    message = render_to_string(
        template_name="admin_notification.html",
        context={
            "notification": notification,
        },
    )

    email_send = EmailMessage(subject="sle3pinghood", body=message, to=[settings.EMAIL_HOST_USER])
    email_send.content_subtype = "html"
    email_send.send(fail_silently=settings.EMAIL_FAIL_SILENTLY)
