from celery import shared_task

from payment.services.emails import send_order_email, send_order_client_email


@shared_task
def send_order_email_task(total, cart_items, name, surname, phone_number, email, city, department, description):
    send_order_email(email=email, description=description, total=total, cart_items=cart_items, name=name,
                     surname=surname, phone_number=phone_number, city=city, department=department)
    send_order_client_email(cart_items=cart_items, name=name, email=email, department=department, city=city)
