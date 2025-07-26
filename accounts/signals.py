from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import account
from django.conf import settings





@receiver(post_save,sender=account)
def send_welcome_email(sender,instance,created,**kwrags):
     if created:
          subject = "welcome to our shop"
          message = f"Hi{instance.username} \n thank you for creating an account with us"
          from_email = settings.DEFAULT_FROM_EMAIL
          user_email = [instance.email]
          send_mail(subject,message,from_email,user_email)
          




