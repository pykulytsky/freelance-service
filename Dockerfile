FROM python:3.9.2-slim

RUN  apt-get update && apt install -y libpq-dev gcc && rm -rf /var/lib/{apt,dpkg,cache,log}/

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt --no-cache-dir
RUN pip3 install uwsgi --no-cache-dir

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POSTGRES_DB_HOST 'db'

COPY . ./app/
