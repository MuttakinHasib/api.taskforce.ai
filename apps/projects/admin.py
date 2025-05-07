from django.contrib import admin

from apps.projects.models.project import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")
    list_per_page = 10


admin.site.register(Project, ProjectAdmin)
