from django.urls import path

from apps.teams.views import TeamView

urlpatterns = [
    path("", TeamView.as_view(), name="teams"),
]
