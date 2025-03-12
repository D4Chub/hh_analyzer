from skills_stats.models import Vacancy, VacancyKeywords


class VacancyRepositories:
    @staticmethod
    def get_all():
        return Vacancy.objects.all()

    @staticmethod
    def get_by_id(vacancy_id):
        return Vacancy.objects.filter(id=vacancy_id)

    @staticmethod
    def create(vacancy_id, profession, title, published_at, json_data):
        return Vacancy.objects.create(
            vacancy_id=vacancy_id,
            profession=profession,
            title=title,
            published_at=published_at,
            json_data=json_data
        )


class VacancyKeywordsRepositories:
    @staticmethod
    def get_all():
        return VacancyKeywords.objects.all()

    @staticmethod
    def get_or_create(name):
        return VacancyKeywords.objects.get_or_create(name=name)
