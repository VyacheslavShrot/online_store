from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_order_email(total, cart_items, name, surname, phone_number, email, city, department, description):
    message = render_to_string(
        template_name="email.html",
        context={
            "total": total,
            "cart_items": cart_items,
            "name": name,
            "surname": surname,
            "phone_number": phone_number,
            "email": email,
            "city": city,
            "department": department,
            "description": description,
        },
    )

    email_send = EmailMessage(subject="cashyong", body=message, to=[settings.EMAIL_HOST_USER])
    email_send.content_subtype = "html"
    email_send.send(fail_silently=settings.EMAIL_FAIL_SILENTLY)


def send_order_client_email(cart_items, name, email, city, department):
    message = render_to_string(
        template_name="client_email.html",
        context={
            "cart_items": cart_items,
            "name": name,
            "email": email,
            "city": city,
            "department": department,
        },
    )

    email_send = EmailMessage(subject="cashyong", body=message, to=[email])
    email_send.content_subtype = "html"
    email_send.send(fail_silently=settings.EMAIL_FAIL_SILENTLY)
