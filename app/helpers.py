from django.core.mail import send_mail
from django.conf import settings


def send_email(subject, message, to):
    """Helper function to send an email"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to] if isinstance(to, str) else to,
        fail_silently=False,
        auth_user=settings.EMAIL_HOST_USER,
        auth_password=settings.EMAIL_HOST_PASSWORD,
    )