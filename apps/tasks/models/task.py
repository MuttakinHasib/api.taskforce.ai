from django.db import models

from common.models import TaskStatus


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=TaskStatus.choices)
    priority = models.
