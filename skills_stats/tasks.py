from celery import shared_task

from skills_stats.api.services.hh_parser import fetch_vacancies
from skills_stats.models import Profession


@shared_task
def fetch_vacancies_task():
    professions = Profession.objects.all()
    for profession in professions:
        fetch_vacancies(profession)
