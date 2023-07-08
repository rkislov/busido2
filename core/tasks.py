from celery import shared_task
from django.core.mail import send_mail


@shared_task()
def send_mail_task(subject, message, from_email, to_mail):
    return send_mail(subject, message, from_email, [to_mail])
