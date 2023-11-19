FROM python:3.11-slim

RUN mkdir -p app
WORKDIR /app

RUN mkdir -p /app/logs
RUN mkdir -p /app/run

COPY requirements.txt /app/

ADD docker.env /app/.env
ADD . /app/

RUN pip install --user -r requirements.txt


CMD python manage.py migrate && \
    python manage.py populate_db && \
    python manage.py collectstatic --noinput --clear && \
    python -m gunicorn drf_user_demo.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
