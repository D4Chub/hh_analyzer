import logging
from datetime import datetime

import requests

from HHanalyzer.settings import FORMAT
from skills_stats.models import Profession, Vacancy, VacancyKeywords

logging.basicConfig(level=logging.INFO, format=FORMAT)

HEADHUNTER_API = "https://api.hh.ru/"
HEADERS = {"User-Agent": "hh-vacancy-parser"}


# TODO: Доработать, улучшить производительность
def fetch_vacancies(profession: Profession):
    """Получает и сохраняет вакансии в БД для данной профессии"""
    response = requests.get(
        url=f"{HEADHUNTER_API}vacancies",
        params={"text": profession.search_query, "per_page": 20},
        headers=HEADERS
    )

    vacancies_data = response.json().get("items", [])

    for vacancy in vacancies_data:
        vacancy_id = vacancy["id"]
        vacancy_title = vacancy["name"]

        vacancy_response = requests.get(f"{HEADHUNTER_API}vacancies/{vacancy_id}", headers=HEADERS)
        vacancy_detail = vacancy_response.json()

        # Преобразование строки с датой в объект datetime с учетом часового пояса
        published_at_str = vacancy_detail.get("published_at")
        published_at = datetime.fromisoformat(published_at_str)

        # Сохранение вакансии в БД
        vacancy_obj, created = Vacancy.objects.update_or_create(
            vacancy_id=vacancy_id,
            defaults={
                "profession": profession,
                "title": vacancy_title,
                "published_at": published_at,
                "json_data": vacancy_detail
            }
        )

        # Обработка ключевых навыков
        key_skills = vacancy_detail.get("key_skills", [])
        for skill in key_skills:
            skill_name = skill["name"]
            skill_obj, _ = VacancyKeywords.objects.get_or_create(name=skill_name)
            vacancy_obj.key_skills.add(skill_obj)


def main():
    professions = Profession.objects.all()
    if not professions:
        logging.warning("Нет профессий в базе данных")
        return

    logging.info(f"Начинаем обновление вакансий для {len(professions)} профессий")
    for profession in professions:
        logging.info(f"Обрабатываем профессию: {profession.name}")
        fetch_vacancies(profession)

    logging.info("Обновление вакансий завершено")


if __name__ == "__main__":
    main()
