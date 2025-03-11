import logging

from celery import shared_task

from HHanalyzer.settings import FORMAT
from skills_stats.api.services.hh_parser import fetch_vacancies_for_profession, process_vacancies
from skills_stats.models import Profession

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=FORMAT)


@shared_task
def fetch_vacancies_task():
    professions = Profession.objects.all()
    for profession in professions:
        logging.info(f"Обрабатываем профессию: {profession.name}")
        process_vacancies(profession, fetch_vacancies_for_profession(profession))

    logging.info("Обновление вакансий завершено")
