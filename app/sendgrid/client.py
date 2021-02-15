from typing import Optional
from .http import SendgridHTTP
from .mail import SendgridMail

from django.conf import settings


class SendgridAPIClient():

    def __init__(self) -> None:
        self.http = SendgridHTTP()

    def send(self, mail: SendgridMail):
        return self.http.post('/mail/send', mail.to_json())

    def send_verification_mail(self, receiver_email: str, dynamic_template_data: Optional[dict]):
        mail = SendgridMail(
            template_id=settings.SENDGRID_VERIFY_EMAIL_TEMPLATE_ID,
            receiver_email=receiver_email,
            subject="Please verify your account",
            dynamic_template_data=dynamic_template_data
        )
        return self.send(mail)

    def send_email_after_job_create_to_creator(self, receiver_email: str, dynamic_template_data: Optional[dict]):
        mail = SendgridMail(
            template_id=settings.SENDGRID_AFTER_JOB_CREATE_TEMPLATE_ID,
            receiver_email=receiver_email,
            subject="Please verify your account",
            dynamic_template_data=dynamic_template_data
        )
        return self.send(mail)
