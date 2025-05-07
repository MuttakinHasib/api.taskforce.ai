from django.contrib import admin

from apps.teams.models import Team, TeamMember


class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner")
    search_fields = ("name", "owner")
    list_per_page = 10


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "team", "role")
    search_fields = ("user", "team", "role")
    list_per_page = 10
    list_filter = ("team", "role")


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
