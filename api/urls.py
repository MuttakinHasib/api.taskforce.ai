from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.authentication.urls")),
    path("teams/", include("apps.teams.urls")),
    path("users/", include("apps.users.urls")),
]
