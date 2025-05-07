from django.contrib import admin

from apps.tasks.models.task import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "priority", "due_date")
    list_filter = ("status", "priority")
    search_fields = ("title", "description")
    list_per_page = 10


# Register your models here.
admin.site.register(Task, TaskAdmin)
