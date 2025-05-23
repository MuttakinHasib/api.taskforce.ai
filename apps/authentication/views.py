from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.serializers import RegisterSerializer


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Register a new user",
        request_body=RegisterSerializer,
        responses={201: RegisterSerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
