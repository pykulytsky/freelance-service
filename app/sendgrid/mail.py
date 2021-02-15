from typing import Optional, Union
from dataclasses import dataclass

from django.conf import settings


@dataclass
class SendgridMail():
    template_id: str
    receiver_email: Union[str, list]
    subject: str
    dynamic_template_data: dict
    sender_email: str = settings.EMAIL_HOST_USER

    def to_json(self):
        data = {
            "personalizations": [{
                "to": [{'email': mail} for mail in self.receiver_email] if isinstance(self.receiver_email, list) else [{'email': self.receiver_email}],
                "dynamic_template_data": self.dynamic_template_data,
                "subject": self.subject,

            }],
            "template_id": self.template_id,
            "from": {
                "email": self.sender_email,
                "name": "Oleh Pykulytsky"
            }
        }

        return data
