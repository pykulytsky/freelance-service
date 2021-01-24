from django.template.loader import get_template
from app.celery import app
from django.core.mail import get_connection, EmailMessage

from django.conf import settings


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
        verification_code
    ):
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
