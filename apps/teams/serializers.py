from rest_framework import serializers

from apps.teams.models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class TeamListSerializer(serializers.Serializer):
    """
    Serializer for documenting paginated team responses in Swagger.
    This represents the structure returned by PageNumberPagination.
    """

    count = serializers.IntegerField(help_text="Total number of teams across all pages")
    next = serializers.URLField(
        required=False,
        allow_null=True,
        help_text="URL to the next page of results, null if this is the last page",
    )
    previous = serializers.URLField(
        required=False,
        allow_null=True,
        help_text="URL to the previous page of results, null if this is the first page",
    )
    results = TeamSerializer(many=True, help_text="List of teams for the current page")
