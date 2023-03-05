import smtplib
import ssl
from email.message import EmailMessage
from django.conf import settings


def sendemail(body, subject, receiver):
    email_sender = 'diacarehacktj@gmail.com'
    email_password = settings.EMAIL_PASSWORD
    email_receiver = receiver

    for x in range(1):
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        body = """
        hiiuhi test
        """ + str(x)
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
