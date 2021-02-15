from django.template.loader import get_template
from app.celery import app
from django.core.mail import get_connection, EmailMessage

from django.conf import settings

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


@app.task
def send_verification_mail_test(mail: EmailMessage):
    if isinstance(mail, EmailMessage):
        raise TypeError("Mail is not EmailMessage object.")

    conn = get_connection(backend=settings.EMAIL_BACKEND)

    try:
        conn.open()
    except Exception:
        raise ValueError("Error while open connection")

    sent = mail.send()
    conn.close()

    return sent


@app.task
def send_verification_mail(
        receiver_email,
        verification_link,
        verification_code):
    template = get_template('authentication/mail.html')
    context = {
        'verification_link': verification_link,
        'verification_code': verification_code
    }
    content = template.render(context)
    msg = EmailMessage(
        'Please verify your account',
        content,
        settings.EMAIL_HOST_USER,
        to=[receiver_email]
    )
    msg.content_subtype = 'html'
    _email = msg.send()

    return _email


@app.task
def send_verification_email_by_sendgrid(
    receiver_email: str,
    verification_link: str,
    receiver_first_name: str
):
    message = Mail(
    from_email=settings.EMAIL_HOST_USER,
    to_emails=receiver_email,
    subject='Please verify your link',
    )
    message.dynamic_tamplate_data = {
        'verification_link': verification_link,
        'first_name': receiver_first_name
    }
    message.template_id = settings.SENDGRID_VERIFY_EMAIL_TEMPLATE_ID

    sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = sendgrid_client.send(message)

    return response.status_code
