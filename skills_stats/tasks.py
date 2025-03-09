import logging

from celery import shared_task

from HHanalyzer.settings import FORMAT
from skills_stats.api.services.hh_parser import fetch_vacancies
from skills_stats.models import Profession

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=FORMAT)


@shared_task
def fetch_vacancies_task():
    #TODO: Доработать запрос
    professions = Profession.objects.get(pk=2)

    logging.info(f"Начинаем обновление вакансий для {len(professions)} профессий")

    for profession in professions:
        logging.info(f"Обрабатываем профессию: {profession.name}")
        fetch_vacancies(profession)
        logging.info(f"Обновление вакансий завершено для профессии: {profession.name}")

    logging.info("Обновление вакансий завершено")
