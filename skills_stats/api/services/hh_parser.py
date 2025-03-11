import logging
from datetime import datetime

import requests

from HHanalyzer.settings import FORMAT
from skills_stats.models import Profession, Vacancy, VacancyKeywords

# Настройки логирования
logging.basicConfig(level=logging.INFO, format=FORMAT)

# API для получения вакансий
HEADHUNTER_API = "https://api.hh.ru/"
HEADERS = {"User-Agent": "hh-vacancy-parser"}


# TODO: Вынести все функции в отдельный класс
# Функция для получения всех вакансий по профессии
def fetch_vacancies_for_profession(profession: Profession):
    logging.info(f"Получаем вакансии для профессии: {profession.name}")

    # Запрос на получение вакансий
    response = requests.get(
        url=f"{HEADHUNTER_API}vacancies",
        params={"text": profession.search_query, "per_page": 20},
        headers=HEADERS
    )
    vacancies_data = response.json().get("items", [])

    if not vacancies_data:
        logging.warning(f"Нет вакансий для профессии: {profession.name}")
        return []

    # Сбор всех id вакансий
    vacancy_ids = [vacancy["id"] for vacancy in vacancies_data]
    return vacancy_ids


# Функция для получения подробной информации по каждой вакансии
def fetch_vacancy_details(vacancy_id):
    url = f"{HEADHUNTER_API}vacancies/{vacancy_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json()


# Функция для обработки и сохранения вакансий в БД
def process_vacancies(profession: Profession, vacancy_ids):
    existing_keywords = {k.name: k for k in VacancyKeywords.objects.all()}

    # Список для хранения новых вакансий и ключевых навыков
    new_vacancies = []

    for vacancy_id in vacancy_ids:
        vacancy_detail = fetch_vacancy_details(vacancy_id)

        vacancy_title = vacancy_detail.get("name")
        published_at_str = vacancy_detail.get("published_at")
        published_at = datetime.fromisoformat(published_at_str) if published_at_str else None

        # Проверяем, существует ли уже вакансия с таким ID
        existing_vacancies = Vacancy.objects.filter(vacancy_id=vacancy_id)

        if existing_vacancies.exists():

            # Используем update_or_create для всех найденных записей
            for existing_vacancy in existing_vacancies:
                existing_vacancy.title = vacancy_title
                existing_vacancy.published_at = published_at
                existing_vacancy.json_data = vacancy_detail
                existing_vacancy.save()

            vacancy_obj = existing_vacancies.first()
        else:
            # Если вакансии с таким ID нет в базе, создаём новую
            vacancy_obj = Vacancy.objects.create(
                vacancy_id=vacancy_id,
                profession=profession,
                title=vacancy_title,
                published_at=published_at,
                json_data=vacancy_detail,
            )

        # Обработка ключевых навыков
        key_skills = vacancy_detail.get("key_skills", [])
        for skill in key_skills:
            skill_name = skill["name"]
            skill_obj, _ = VacancyKeywords.objects.get_or_create(name=skill_name)
            vacancy_obj.key_skills.add(skill_obj)

        # Добавляем вакансию в список для обновления
        new_vacancies.append(vacancy_obj)

    return new_vacancies
