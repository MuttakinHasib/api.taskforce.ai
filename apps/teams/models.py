from uuid import uuid4

from django.db import models

from apps.users.models import User
from common.models import TeamRole


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_teams"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams")
    role = models.CharField(max_length=20, choices=TeamRole.choices)

    class Meta:
        unique_together = ("team", "user")
