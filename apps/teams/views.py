

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.teams.filters import TeamFilter
from apps.teams.models import Team
from apps.teams.paginations import TeamPagination
from apps.teams.serializers import TeamListSerializer, TeamSerializer, TeamCreateSerializer, TeamUpdateSerializer


class TeamView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    pagination_class = TeamPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = TeamFilter

    @swagger_auto_schema(
        tags=["Teams"],
        operation_description="Get all teams with pagination and search/filter",
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search teams by name (case-insensitive partial match)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Number of teams per page (max 100)",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
        ],
        responses={
            200: TeamListSerializer,
            401: "Unauthorized - Authentication credentials were not provided",
            403: "Forbidden - You do not have permission to perform this action",
        },
    )
    def get(self, request):
        teams = Team.objects.filter(owner=request.user)

        # Apply filters using django-filter
        filter_set = self.filter_class(request.GET, queryset=teams)
        if filter_set.is_valid():
            teams = filter_set.qs

        # Apply pagination
        paginator = self.pagination_class()
        paginated_teams = paginator.paginate_queryset(teams, request)

        serializer = self.serializer_class(paginated_teams, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        tags=["Teams"],
        operation_description="Create a new team",
        request_body=TeamCreateSerializer,
        responses={
            201: TeamSerializer,
            400: "Bad Request - Invalid input data",
            401: "Unauthorized - Authentication credentials were not provided",
            403: "Forbidden - You do not have permission to perform this action",
        },
    )
    def post(self, request):
        serializer = TeamCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Set the owner to the logged-in user
            team = serializer.save(owner=request.user)
            # Return the created team using the full serializer for response
            response_serializer = TeamSerializer(team)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Teams"],
        operation_description="Get a specific team by ID",
        responses={
            200: TeamSerializer,
            401: "Unauthorized - Authentication credentials were not provided",
            403: "Forbidden - You do not have permission to perform this action",
            404: "Not Found - Team not found or you don't have permission to access it"
        },
    )
    def get(self, request, pk):
        try:
            team = Team.objects.get(pk=pk, owner=request.user)
        except Team.DoesNotExist:
            return Response(
                {"error": "Team not found or you don't have permission to access it"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Teams"],
        operation_description="Update a specific team (full update)",
        request_body=TeamUpdateSerializer,
        responses={
            200: TeamSerializer,
            400: "Bad Request - Invalid input data",
            401: "Unauthorized - Authentication credentials were not provided",
            403: "Forbidden - You do not have permission to perform this action",
            404: "Not Found - Team not found or you don't have permission to update it"
        },
    )
    def put(self, request, pk):
        try:
            team = Team.objects.get(pk=pk, owner=request.user)
        except Team.DoesNotExist:
            return Response(
                {"error": "Team not found or you don't have permission to update it"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = TeamUpdateSerializer(team, data=request.data, partial=False)
        if serializer.is_valid():
            updated_team = serializer.save()
            response_serializer = TeamSerializer(updated_team)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["Teams"],
        operation_description="Update a specific team (partial update)",
        request_body=TeamUpdateSerializer,
        responses={
            200: TeamSerializer,
            400: "Bad Request - Invalid input data",
            401: "Unauthorized - Authentication credentials were not provided",
            403: "Forbidden - You do not have permission to perform this action",
            404: "Not Found - Team not found or you don't have permission to update it"
        },
    )
    def patch(self, request, pk):
        try:
            team = Team.objects.get(pk=pk, owner=request.user)
        except Team.DoesNotExist:
            return Response(
                {"error": "Team not found or you don't have permission to update it"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = TeamUpdateSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            updated_team = serializer.save()
            response_serializer = TeamSerializer(updated_team)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["Teams"],
        operation_description="Delete a specific team",
        responses={
            204: "No Content - Team successfully deleted",
            401: "Unauthorized - Authentication credentials were not provided",
            403: "Forbidden - You do not have permission to perform this action",
            404: "Not Found - Team not found or you don't have permission to delete it"
        },
    )
    def delete(self, request, pk):
        try:
            team = Team.objects.get(pk=pk, owner=request.user)
        except Team.DoesNotExist:
            return Response(
                {"error": "Team not found or you don't have permission to delete it"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
