from app.celery import app
from django.utils.module_loading import import_string
from django.conf import settings


@app.task
def update_exchange(
        backend=settings.EXCHANGE_BACKEND,
        **kwargs):
    backend = import_string(backend)()
    backend.update_rates(**kwargs)
