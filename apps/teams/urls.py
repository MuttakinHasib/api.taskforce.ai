from django.urls import path

from apps.teams.views import TeamView, TeamDetailView

urlpatterns = [
    path("", TeamView.as_view(), name="teams"),
    path("<uuid:pk>/", TeamDetailView.as_view(), name="team-detail"),
]
