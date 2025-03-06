from django.db import models


class Profession(models.Model):
    """Модель профессии"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'


class SearchQuery(models.Model):
    """Модель для поискового запроса"""
    query = models.CharField(max_length=100)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.query} - {self.profession}"

    class Meta:
        verbose_name = 'Поисковый запрос'
        verbose_name_plural = 'Поисковые запросы'


class VacancyKeywords(models.Model):
    """Модель ключевых навыков из вакансий"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ключевой навык'
        verbose_name_plural = 'Ключевые навыки'
