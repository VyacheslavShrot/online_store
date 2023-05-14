from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_registration_email(total, cart_items, name, surname, phone_number, email, city, department, description):
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

    email = EmailMessage(subject="New Order", body=message, to=[settings.EMAIL_HOST_USER])
    email.content_subtype = "html"
    email.send(fail_silently=settings.EMAIL_FAIL_SILENTLY)
