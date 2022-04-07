FROM python:3.9-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y cron
COPY . .

EXPOSE 8000

RUN ["chown", ":www-data","/code"]
RUN ["chown", ":www-data", "/code/db.sqlite3"]
RUN ["chmod", "664", "/code/db.sqlite3"]
RUN ["python3", "manage.py", "makemigrations"]
RUN ["python3", "manage.py", "migrate"]
RUN ["python3", "manage.py", "crontab","add"]
RUN ["python3", "manage.py", "crontab","show"]
RUN ["python3", "manage.py", "makemigrations"]
RUN ["python3", "manage.py", "migrate"]

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
