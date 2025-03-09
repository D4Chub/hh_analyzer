from django.urls import path

from skills_stats.api.v1.views import KeySkillsCountView

app_name = 'skills_stats'

urlpatterns = [
    path("profession/<int:profession_id>/skills/", KeySkillsCountView.as_view(), name="skills_count"),
]
