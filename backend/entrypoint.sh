#!/bin/bash

# Ожидание готовности базы данных
echo "Ожидание запуска базы данных..."
if [ "$DB_ENGINE" = "django.db.backends.postgresql" ]; then
  # Проверка доступности PostgreSQL с увеличенным таймаутом
  max_attempts=30
  counter=0
  until PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c '\q' || [ $counter -ge $max_attempts ]; do
    echo "PostgreSQL недоступен - попытка $counter/$max_attempts, ожидание..."
    counter=$((counter+1))
    sleep 3
  done
  
  if [ $counter -ge $max_attempts ]; then
    echo "Ошибка: PostgreSQL недоступен после $max_attempts попыток"
    exit 1
  else
    echo "PostgreSQL запущен"
  fi
fi

# Применение миграций
echo "Применение миграций..."
python manage.py migrate

# Сбор статических файлов
echo "Сбор статических файлов..."
python manage.py collectstatic --noinput

# Создание суперпользователя, если его нет
echo "Проверка наличия суперпользователя..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0) if User.objects.filter(is_superuser=True).exists() else User.objects.create_superuser('admin@example.com', 'admin123', name='Admin')"
if [ $? -eq 0 ]; then
  echo "Суперпользователь уже существует"
else
  echo "Создан суперпользователь admin с паролем admin123"
fi

# Запуск сервера
echo "Запуск сервера..."
exec gunicorn speech_school.wsgi:application --bind 0.0.0.0:8000 