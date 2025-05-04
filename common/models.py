from django.db import models


class TaskStatus(models.TextChoices):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(models.TextChoices):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TeamRole(models.TextChoices):
    ADMIN = "admin"
    MEMBER = "member"
