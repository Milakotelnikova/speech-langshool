# Speech School Backend

Django-бэкенд для сайта школы иностранных языков.

## Инструкция по запуску проекта "Speech School"

### Запуск через Docker

1. Убедитесь, что на вашем компьютере установлены Docker и Docker Compose

2. Склонируйте репозиторий и перейдите в его корневую директорию

3. Запустите проект с помощью Docker Compose:
   ```
   docker-compose up -d
   ```

4. После запуска приложение будет доступно по адресу:
   - Бэкенд API: http://localhost:8000
   - База данных PostgreSQL: localhost:5432
     - Имя БД: speech_school_db
     - Пользователь: postgres
     - Пароль: postgres

5. По умолчанию будет создан суперпользователь:
   - Email: admin@example.com
   - Пароль: admin123

6. Для остановки проекта:
   ```
   docker-compose down
   ```

7. Для удаления всех данных (включая базу):
   ```
   docker-compose down -v
   ```

### Локальный запуск (без Docker)

1. Убедитесь, что у вас установлены:
   - Python 3.10 или выше
   - Poetry
   - PostgreSQL

2. Склонируйте репозиторий и перейдите в директорию backend

3. Установите зависимости с помощью Poetry:
   ```
   poetry install
   ```

4. Настройте локальную базу данных PostgreSQL:
   - Создайте базу данных: speech_school_db
   - Обновите файл .env:
     ```
     DB_HOST=localhost  # Измените с db на localhost
     ```

5. Активируйте виртуальное окружение:
   ```
   poetry shell
   ```

6. Примените миграции:
   ```
   poetry run python manage.py migrate
   ```

7. Соберите статические файлы:
   ```
   poetry run python manage.py collectstatic --noinput
   ```

8. Создайте суперпользователя:
   ```
   poetry run python manage.py createsuperuser
   ```

9. Запустите сервер разработки:
   ```
   poetry run python manage.py runserver
   ```

10. Приложение будет доступно по адресу http://localhost:8000

### Доступ к API и документации

После запуска проекта документация API будет доступна по адресу:
- http://localhost:8000/api/schema/swagger-ui/
- http://localhost:8000/api/schema/redoc/

### Примечания

- В файле .env находятся настройки проекта, включая параметры подключения к базе данных и почте
- Проект использует Django 5, Django REST framework и PostgreSQL
- При запуске в Docker создаются директории media и static, для хранения загружаемых файлов и статических ресурсов 

### Вход в административную панель Django

После запуска проекта панель администратора Django будет доступна по адресу:
- http://localhost:8000/admin/

Данные для входа:
- Email: admin@example.com
- Пароль: admin123 (если вы запускали через Docker)
- или данные, которые вы указали при создании суперпользователя (если запускали локально)

### Запуск тестов

#### Запуск тестов локально

1. Активируйте виртуальное окружение:
   ```
   poetry shell
   ```

2. Запустите все тесты:
   ```
   poetry run python manage.py test
   ```

3. Запуск тестов для конкретного приложения:
   ```
   poetry run python manage.py test accounts
   ```

4. Запуск с покрытием кода:
   ```
   poetry run coverage run --source='.' manage.py test
   poetry run coverage report
   ```

#### Запуск тестов в Docker

1. Запуск всех тестов:
   ```
   docker-compose exec backend python manage.py test
   ```

2. Запуск тестов для конкретного приложения:
   ```
   docker-compose exec backend python manage.py test accounts
   ``` 