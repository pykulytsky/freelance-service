FROM python:3.9.2-slim-buster

RUN  apt-get update && apt install -y build-essential libpq-dev

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV POSTGRESQL_HOST 172.17.0.1/16

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

EXPOSE 8000

CMD [ "python3", "app/manage.py", "runserver" ]
