FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=monitoring.settings

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "monitoring.wsgi:application"]