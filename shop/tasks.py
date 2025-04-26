
from celery import shared_task
from django.conf import settings
from celery import shared_task 
from django.core.mail import send_mail

@shared_task
def sendmessage(subject,message_body,email):
    # Send email to admin
            send_mail(
                subject,
                message_body,
                email,  # from email (user's email)
                [settings.ADMIN_EMAIL],  # to admin's email
            )