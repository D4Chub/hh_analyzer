#!/bin/bash

# Сборка и запуск
docker compose up --build -d

# Создание миграций
docker compose exec web python manage.py migrate

# Загрузка тестовых данных
docker compose exec web python manage.py loaddata test_data.json

# Вызов celery задачи для парсинга вакансий
docker compose exec web celery -A HHanalyzer call skills_stats.tasks.fetch_vacancies_task
