from typing import Union
from dataclasses import dataclass
from authentication.models import User
import uuid

from django.conf import settings


@dataclass
class SendgridMail():
    """Class for easy conversion of email data to json."""
    template_id: str
    receiver_email: Union[str, list]
    receiver_name: str
    subject: str
    dynamic_template_data: dict
    sender_email: str = settings.EMAIL_HOST_USER
    sender_name: str = settings.EMAIL_HOST_USER_NAME

    def to_json(self):
        data = {
            "personalizations": [{
                "to": [{'email': mail} for mail in self.receiver_email] if isinstance(self.receiver_email, list) else [{'email': self.receiver_email, 'name': self.receiver_name}],
                "dynamic_template_data": self.dynamic_template_data,
                "subject": self.subject,

            }],
            "template_id": self.template_id,
            "from": {
                "email": self.sender_email,
                "name": self.sender_email
            }
        }

        return data


@dataclass
class Receiver():
    """Class implements the user model for the service Sendgrid."""
    first_name: str
    last_name: str
    email: str
    verification_code: uuid

    @classmethod
    def from_user_model(cls, user: User):
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            verification_code=user.email_verification_code
        )

    def to_json_email_verification(self):
        return {
            'first_name': self.first_name,
            'verification_link': 'http://localhost:8080/verify/' + str(self.verification_code),
        }
