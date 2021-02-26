from authentication.models import User
from sendgrid.client import SendgridAPIClient
from sendgrid.mail import Receiver
from app.celery import app
from django.utils.module_loading import import_string
from django.conf import settings
from django.utils import timezone

from .models import Job


@app.task
def update_exchange(
        backend=settings.EXCHANGE_BACKEND,
        **kwargs):
    backend = import_string(backend)()
    backend.update_rates(**kwargs)


@app.task
def send_email_after_create_job(
    user_id: int,
    job_id: int
):
    if not settings.DEBUG:
        receiver = Receiver.from_user_model(User.objects.get(id=user_id))
        job = Job.objects.get(id=job_id)
        data = receiver.to_json_after_create_job(job)

        client = SendgridAPIClient()
        response = client.send_email_after_job_create_to_creator(
            receiver_email=receiver.email,
            dynamic_template_data=data
        )

        return response.status_code
