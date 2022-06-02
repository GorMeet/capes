FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev

RUN pip install -r requirements.txt
COPY . ./code

EXPOSE 8000

#RUN python3 manage.py makemigrations
#RUN python3 manage.py migrate


CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
