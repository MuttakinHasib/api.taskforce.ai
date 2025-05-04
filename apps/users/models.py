from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserAccount(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    avatar = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
