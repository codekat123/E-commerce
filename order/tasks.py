from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order


@shared_task
def send_mails(order_id) -> str:
     order = Order.objects.get(order_id = order_id)
     subject = f"id Order : {order.order_id}"
     message = f"Dear :{order.get_full_name()} \n you've successfully placed order. \n your order id is : {order.order_id}"
     mail_send = send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[order.email])
     return mail_send