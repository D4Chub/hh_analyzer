from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from skills_stats.models import VacancyKeywords


class KeySkillsCountView(APIView):
    def get(self, request, profession_id):
        key_skills = VacancyKeywords.objects.filter(vacancies__profession_id=profession_id).annotate(
            count=Count('vacancies')).order_by('-count').values('id', 'name', 'count')

        return Response(key_skills)
