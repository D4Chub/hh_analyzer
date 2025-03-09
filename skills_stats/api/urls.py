from django.urls import include, path

urlpatterns = [
    path("v1/skills_stats/", include("skills_stats.api.v1.urls", namespace="skills_stats_v1")),
]
