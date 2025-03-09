📝 О проекте
============

Данный проект предназначен для анализа ключевых навыков по профессии на hh.ru.  


---

🛠 Стэк
=======

- Python
- Django
- Django Rest Framework
- Celery
- Redis
- Docker
- Docker Compose
- PostgreSQL

---

🚀 Запуск проекта
=================

1. Клонируем репозиторий и переходим в директорию:


```bash 
  git clone https://github.com/D4Chub/hh_analyzer.git
  cd hh_analyzer
```

2. Выполняем bash скрипт

```bash
  bash startup.sh
```

После выполнения этих шагов:

- Проект будет запущен.
- В базе данных появятся тестовые данные (профессии).
- Запустится задача Celery, которая активирует парсер.
- Через 10-15 секунд в базе данных появятся данные о вакансиях.

---

📡 API
=====

Приложение предоставляет 1 эндпоинт:

```bash
   http://localhost:8000/api/v1/skills_stats/profession/{id}/skills/
```

Чтобы протестировать, можете перейти по ссылке:

```bash
   http://localhost:8000/api/v1/skills_stats/profession/1/skills/
```

Эндпоинт возвращает список ключевых навыков и их количество, которые встречаются в вакансиях данной профессии.
Вот как это выглядит для профессии "Python Developer":

```json
[
    {
        "id": 1,
        "name": "Python",
        "count": 5
    },
    {
        "id": 2,
        "name": "Django",
        "count": 3
    },
    {
        "id": 3,
        "name": "FastAPI",
        "count": 2
    },
    {
        "id": 4,
        "name": "Flask",
        "count": 2
    }
]
```
---

📝 TODO
====
- Добавить тесты
- Изменить парсер (вынести логику в отдельный класс)
- Добавить документацию OpenAPI swagger

---