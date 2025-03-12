from datetime import datetime
from typing import List, Optional, Any

from skills_stats.models import Vacancy, VacancyKeywords


class VacancyRepositories:
    def get_all(self) -> List[Vacancy]:
        return Vacancy.objects.all()

    def get_by_id(self, vacancy_id) -> Optional[Vacancy]:
        return Vacancy.objects.filter(id=vacancy_id).first()

    def create(
            self,
            vacancy_id: int,
            profession: Any,
            title: str,
            published_at: datetime,
            json_data: dict
    ) -> Vacancy:
        return Vacancy.objects.create(
            vacancy_id=vacancy_id,
            profession=profession,
            title=title,
            published_at=published_at,
            json_data=json_data
        )


class VacancyKeywordsRepositories:
    def get_all(self) -> List[VacancyKeywords]:
        return VacancyKeywords.objects.all()

    def get_or_create(self, name: str) -> VacancyKeywords:
        keyword, _ = VacancyKeywords.objects.get_or_create(name=name)
        return keyword
