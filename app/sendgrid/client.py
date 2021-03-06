from typing import Callable, Optional

from django.conf import settings

from .http import SendgridHTTP
from .mail import Receiver, SendgridMail


class SendgridAPIClient():

    def __init__(self) -> None:
        self.http = SendgridHTTP()

    def send(self, template_id: str, receiver_email: str, dynamic_template_data: Optional[dict], subject: str, receiver_name: str):
        mail = SendgridMail(
            template_id=template_id,
            receiver_email=receiver_email,
            subject=subject,
            receiver_name=receiver_name,
            dynamic_template_data=dynamic_template_data
        )

        return self.http.post('/mail/send', mail.to_json())

    def send_verification_mail(self, receiver: Receiver) -> Callable[[str, str, Optional[dict], str, str], SendgridMail]:

        return self.send(
            template_id=settings.SENDGRID_VERIFY_EMAIL_TEMPLATE_ID,
            receiver_email=receiver.email,
            subject="Please verify your account",
            dynamic_template_data={
                **receiver.to_json_email_verification()
            },
            receiver_name=receiver.first_name + ' ' + receiver.last_name
        )

    def send_email_after_job_create_to_creator(self, receiver_email: str, dynamic_template_data: Optional[dict]) -> Callable[[str, str, Optional[dict], str, str], SendgridMail]:
        return self.send(
            template_id=settings.SENDGRID_AFTER_JOB_CREATE_TEMPLATE_ID,
            receiver_email=receiver_email,
            subject="You just create new job",
            dynamic_template_data=dynamic_template_data
        )

    def send_new_password(self, receiver: Receiver, password: str, ip_addr: str) -> Callable[[str, str, Optional[dict], str, str], SendgridMail]:
        return self.send(
            template_id=settings.SENDGRID_SEND_NEW_PASSWORD_TEMPLATE_ID,
            receiver_email=receiver.email,
            subject="You just, reset your password",
            dynamic_template_data={
                **receiver.to_json_reset_password(password, ip_addr)
            },
            receiver_name=receiver.first_name + ' ' + receiver.last_name
        )
