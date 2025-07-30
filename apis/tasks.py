from celery import shared_task
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from accounts.models import account
from django.shortcuts import get_object_or_404

@shared_task
def verification(user_id):
    user = get_object_or_404(account, id=user_id)
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    subject = "Please activate your account"
    activation_link = f'http://127.0.0.1:8000/v1/api/activation/{uid}/{token}/'
    message = f"Hi {user.first_name},\n\nPlease click the link below to activate your account:\n{activation_link}"

    send_email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    send_email.send()

    return 'Activation email sent'
