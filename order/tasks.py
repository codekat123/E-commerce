from celery import shared_task
from django.core.mail import send_mail , EmailMessage
from django.conf import settings
from .models import Order
from django.template.loader import render_to_string
import weasyprint
from io import BytesIO


@shared_task
def send_mails(order_id) -> str:
     order = Order.objects.get(order_id = order_id)
     subject = f"id Order : {order.order_id}"
     message = f"Dear :{order.get_full_name()} \n you've successfully placed order. \n your order id is : {order.order_id}"
     mail_send = send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[order.email])
     return mail_send

@shared_task
def send_invoice(order_id):
     order = Order.objects.get(order_id=order_id)
     subject = f"my shop - invoice - {order.order_id}"
     message = f"Hello {order.get_full_name()} \n please find attached the invoice for your recent purchase"
     from_email = settings.DEFAULT_FROM_EMAIL
     to_email = [order.email]
     html = render_to_string('order/pdf.html',{'order':order})
     out = BytesIO()
     weasyprint.HTML(string=html).write_pdf(out)

     email = EmailMessage(
          subject = subject,
          from_email = from_email,
          body=message,
          to = to_email,
     )
     email.attach(f'order_{order.order_id}.pdf',out.getvalue(),'application/pdf')
     email.send()
     return True

