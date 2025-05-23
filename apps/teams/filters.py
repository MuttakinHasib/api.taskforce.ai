import django_filters

from apps.teams.models import Team


class TeamFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Team
        fields = []
