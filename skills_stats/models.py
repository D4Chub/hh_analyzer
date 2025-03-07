from django.db import models


class Profession(models.Model):
    """Модель профессии"""
    name = models.CharField("Название", max_length=100, unique=True)
    search_query = models.CharField("Параметр поиска", max_length=255)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'


class VacancyKeywords(models.Model):
    """Модель ключевых навыков из вакансий"""
    name = models.CharField("Название", max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ключевой навык'
        verbose_name_plural = 'Ключевые навыки'


class Vacancy(models.Model):
    """Модель собранных вакансий"""
    profession = models.ForeignKey(
        Profession,
        verbose_name="Профессия",
        on_delete=models.CASCADE,
        related_name="vacancies"
    )
    vacancy_id = models.IntegerField("ID вакансии")
    title = models.CharField("Название вакансии", max_length=100)
    key_skills = models.ManyToManyField(
        VacancyKeywords,
        verbose_name="Ключевые навыки",
        related_name="vacancies"
    )
    published_at = models.DateTimeField("Дата публикации")
    json_data = models.JSONField("Данные в json")

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
