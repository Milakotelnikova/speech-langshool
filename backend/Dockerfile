FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей системы и PostgreSQL-клиента
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей
RUN pip install --upgrade pip && \
    pip install poetry

# Копирование файлов проекта
COPY pyproject.toml poetry.lock ./

# Настройка poetry для создания виртуального окружения в контейнере
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Копирование остальных файлов проекта
COPY . .

# Устанавливаем права на выполнение скрипта entrypoint.sh
RUN chmod +x entrypoint.sh

# Создание статических файлов
RUN python manage.py collectstatic --noinput

# Открытие порта
EXPOSE 8000

# Запуск через entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"] 