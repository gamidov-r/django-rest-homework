FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt update && apt install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python пакеты
RUN pip install --no-cache-dir \
    Pillow \
    redis \
    django \
    djangorestframework \
    python-dotenv \
    psycopg2-binary \
    django-filter \
    djangorestframework-simplejwt \
    drf-yasg \
    stripe \
    celery \
    django-celery-beat \
    gunicorn \
    whitenoise

ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Копируем проект
COPY . /app/

# Создаем директории для статики
RUN mkdir -p /app/static /app/statics

EXPOSE 8000

# Команда по умолчанию (может быть переопределена в docker-compose)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]