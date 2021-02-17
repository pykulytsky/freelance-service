from django.template.loader import get_template
from app.celery import app
from django.core.mail import EmailMessage
from django.utils.module_loading import import_string
from django.conf import settings


@app.task
def update_exchange(
        backend=settings.EXCHANGE_BACKEND,
        **kwargs):
    backend = import_string(backend)()
    backend.update_rates(**kwargs)


@app.task
def send_email_after_create_job(
        receiver_email,
        date,
        job_name,
        deadline):
    template = get_template('jobs/after_job_create.html')
    context = {
        'date': date,
        'job_name': job_name,
        'deadline': deadline,
    }
    content = template.render(context)
    msg = EmailMessage(
        f'You just created job {job_name}',
        content,
        settings.EMAIL_HOST_USER,
        to=[receiver_email]
    )
    msg.content_subtype = 'html'
    _email = msg.send()

    return _email
