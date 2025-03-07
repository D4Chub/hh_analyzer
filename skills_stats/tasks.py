from celery import shared_task

from api.services.hh_parser import fetch_vacancies
from models import Profession


@shared_task
def fetch_vacancies_task():
    professions = Profession.objects.all()
    for profession in professions:
        fetch_vacancies(profession)
