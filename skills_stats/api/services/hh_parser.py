import logging
from datetime import datetime

import requests
from django.db import IntegrityError

from HHanalyzer.settings import FORMAT
from skills_stats.api.services.repositories import VacancyRepositories, VacancyKeywordsRepositories
from skills_stats.models import Profession

# Настройки логирования
logging.basicConfig(level=logging.INFO, format=FORMAT)

# API для получения вакансий
HEADHUNTER_API = "https://api.hh.ru/"
HEADERS = {"User-Agent": "hh-vacancy-parser"}


class HHParser:
    def __init__(
        self,
        profession: Profession,
        vacancy: VacancyRepositories,
        vacancy_keywords: VacancyKeywordsRepositories
    ) -> None:

        self.profession = profession
        self.vacancy = vacancy
        self.vacancy_keywords = vacancy_keywords

    def _response(self, vacancy_id: int = None, search_query: str = None) -> dict:
        url: str = f"{HEADHUNTER_API}vacancies/{vacancy_id}" if vacancy_id else f"{HEADHUNTER_API}vacancy"
        params: dict | None = {"text": search_query, "per_page": 20} if search_query else None

        response = requests.get(
            url=url,
            params=params,
            headers=HEADERS
        )

        if response.status_code != 200:
            logging.error(f"Ошибка при запросе вакансий: {response.status_code}")

        return response.json()

    def fetch_vacancies_ids(self) -> list[int]:
        logging.info(f"Получаем вакансии для профессии: {self.profession.name}")
        logging.info(f"Поиск по запросу: {self.profession.search_query}")

        # TODO: Настроить вызов метода _response
        response = requests.get(
            url=f"{HEADHUNTER_API}vacancies",
            params={"text": self.profession.search_query, "per_page": 20},
            headers=HEADERS
        )
        vacancies_data = response.json().get("items", [])

        if not vacancies_data:
            logging.warning(f"Нет ВАКАНСИЙ для профессии: {self.profession.name}")
            return []

        # Сбор всех id вакансий
        vacancy_ids = [vacancy["id"] for vacancy in vacancies_data]
        return vacancy_ids

    def fetch_vacancy_details(self, vacancy_ids: list[int]) -> None:

        for vacancy_id in vacancy_ids:
            vacancy_detail = self._response(vacancy_id=vacancy_id)

            vacancy_title = vacancy_detail.get("name")
            published_at_str = vacancy_detail.get("published_at")
            published_at = datetime.fromisoformat(published_at_str) if published_at_str else None
            key_skills = vacancy_detail.get("key_skills", [])

            try:
                vacancy = self.vacancy.create(
                    vacancy_id=vacancy_id,
                    profession=self.profession,
                    title=vacancy_title,
                    published_at=published_at,
                    json_data=vacancy_detail
                )
            except IntegrityError:
                continue

            # Получаем существующие в бд навыки
            existing_keywords = {k.name: k for k in self.vacancy_keywords.get_all()}
            for skill in key_skills:
                skill_name = skill["name"]
                if skill_name not in existing_keywords:
                    # Если навыка нет, создаем его и добавляем в словарик
                    existing_keywords[skill_name], _ = self.vacancy_keywords.get_or_create(name=skill_name)

                vacancy.key_skills.add(existing_keywords[skill_name])
