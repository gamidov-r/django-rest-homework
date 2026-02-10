FROM python:3.11-slim as build
WORKDIR /build/
EXPOSE 8000
#ENV PATH="/home/devuser/.local/bin:${PATH}"
ENV POETRY_VIRTUALENVS_CREATE=false
#ENV POETRY_VERSION=1.7.1 \
#    POETRY_HOME="/opt/poetry" \
#    POETRY_VIRTUALENVS_CREATE=false \
#    POETRY_NO_INTERACTION=1

RUN apt update && apt install -y \
    gcc \
    libpq-dev \
    curl \
    celery \
    redis-server \
    python3-poetry \
    python3-poetry-core \
    python3-celery \
    postgresql \
    && rm -rf /var/lib/apt/lists/*

#RUN curl -sSL https://install.python-poetry.org | python3 -
#RUN pip install poetry
#COPY ./poetry.lock ./pyproject.toml /build/
#RUN poetry install --without dev --no-interaction --no-ansi

FROM build as materials


#ENV PATH="${POETRY_HOME}/bin:${PATH}"
#WORKDIR /app

# Копируем файлы зависимостей
#COPY backend/pyproject.toml poetry.lock* ./
#RUN poetry install --no-root --without dev

RUN pip3 install --user Pillow redis django djangorestframework dotenv psycopg2-binary django-filter djangorestframework-simplejwt drf-yasg stripe celery django-celery-beat
RUN pip install --user celery
# Устанавливаем зависимости
#RUN poetry install

# Финальный образ

WORKDIR /app
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV APPLICATION_HOSTNAME='127.0.0.1'

#WORKDIR /app
COPY . .
RUN rm -r /build
#RUN mkdir static

# Копируем зависимости из builder
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin /usr/local/bin


# Копируем код приложения
#COPY . .

# Создаем пользователя для безопасности
#RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
#USER appuser

# Проверяем установку
#RUN python -c "import django; print(f'Django version: {django.__version__}')"

EXPOSE 8000

# Команда запуска
CMD ["psql", "-U", "homework", "-d", "rest", "-f", "create_db.sql"]

#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]