FROM python:3.9.2

RUN  apt-get update && apt install -y libpq-dev tree

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . ./app/
