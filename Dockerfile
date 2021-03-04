FROM python:3.9.2-slim-buster

RUN  apt-get update && apt install -y build-essential libpq-dev

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV POSTGRESQL_HOST host.docker.internal

COPY . .

EXPOSE 5432

CMD [ "python3", "app/manage.py", "runserver" ]
