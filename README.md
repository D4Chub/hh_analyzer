### Запуск проекта

1. Сначала собираем и запускаем контейнеры:

    ```bash
    docker compose up --build
    ```

2. Создаём миграции:

    ```bash
    docker compose exec web python manage.py makemigrations
    ```

3. Применяем миграции:

    ```bash
    docker compose exec web python manage.py migrate
    ```
