FROM python:3.11.2-alpine
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY application /app
WORKDIR /app

CMD gunicorn app:app -b 0.0.0.0:80
