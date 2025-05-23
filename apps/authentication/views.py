from django.conf import settings
from django.contrib.auth import login
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.authentication.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    TokenSerializer,
    UserProfileSerializer,
)


class RegisterView(APIView):
    """User registration endpoint"""

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Register a new user",
        request_body=RegisterSerializer,
        responses={201: TokenSerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate tokens for the new user
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Prepare response data
            response_data = {
                "access": str(access_token),
                "refresh": str(refresh),
                "user": UserProfileSerializer(user).data,
            }

            # Create response
            response = Response(response_data, status=status.HTTP_201_CREATED)

            # Set cookies if configured
            if hasattr(settings, "JWT_AUTH_COOKIE"):
                response.set_cookie(
                    settings.JWT_AUTH_COOKIE,
                    str(access_token),
                    max_age=settings.SIMPLE_JWT[
                        "ACCESS_TOKEN_LIFETIME"
                    ].total_seconds(),
                    httponly=settings.JWT_AUTH_COOKIE_HTTP_ONLY,
                    secure=settings.JWT_AUTH_COOKIE_SECURE,
                    samesite=settings.JWT_AUTH_COOKIE_SAMESITE,
                )

            if hasattr(settings, "JWT_AUTH_REFRESH_COOKIE"):
                response.set_cookie(
                    settings.JWT_AUTH_REFRESH_COOKIE,
                    str(refresh),
                    max_age=settings.SIMPLE_JWT[
                        "REFRESH_TOKEN_LIFETIME"
                    ].total_seconds(),
                    httponly=settings.JWT_AUTH_COOKIE_HTTP_ONLY,
                    secure=settings.JWT_AUTH_COOKIE_SECURE,
                    samesite=settings.JWT_AUTH_COOKIE_SAMESITE,
                )

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """User login endpoint"""

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Login user with email and password",
        request_body=LoginSerializer,
        responses={200: TokenSerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # Update last login
            login(request, user)

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Prepare response data
            response_data = {
                "access": str(access_token),
                "refresh": str(refresh),
                "user": UserProfileSerializer(user).data,
            }

            # Create response
            response = Response(response_data, status=status.HTTP_200_OK)

            # Set cookies if configured
            if hasattr(settings, "JWT_AUTH_COOKIE"):
                response.set_cookie(
                    settings.JWT_AUTH_COOKIE,
                    str(access_token),
                    max_age=settings.SIMPLE_JWT[
                        "ACCESS_TOKEN_LIFETIME"
                    ].total_seconds(),
                    httponly=settings.JWT_AUTH_COOKIE_HTTP_ONLY,
                    secure=settings.JWT_AUTH_COOKIE_SECURE,
                    samesite=settings.JWT_AUTH_COOKIE_SAMESITE,
                )

            if hasattr(settings, "JWT_AUTH_REFRESH_COOKIE"):
                response.set_cookie(
                    settings.JWT_AUTH_REFRESH_COOKIE,
                    str(refresh),
                    max_age=settings.SIMPLE_JWT[
                        "REFRESH_TOKEN_LIFETIME"
                    ].total_seconds(),
                    httponly=settings.JWT_AUTH_COOKIE_HTTP_ONLY,
                    secure=settings.JWT_AUTH_COOKIE_SECURE,
                    samesite=settings.JWT_AUTH_COOKIE_SAMESITE,
                )

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """User logout endpoint"""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Logout user and blacklist refresh token",
        responses={200: "Successfully logged out"},
    )
    def post(self, request):
        try:
            # Get refresh token from request data or cookies
            refresh_token = request.data.get("refresh")
            if not refresh_token and hasattr(settings, "JWT_AUTH_REFRESH_COOKIE"):
                refresh_token = request.COOKIES.get(settings.JWT_AUTH_REFRESH_COOKIE)

            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            # Create response
            response = Response(
                {"message": "Successfully logged out"}, status=status.HTTP_200_OK
            )

            # Clear cookies
            if hasattr(settings, "JWT_AUTH_COOKIE"):
                response.delete_cookie(settings.JWT_AUTH_COOKIE)
            if hasattr(settings, "JWT_AUTH_REFRESH_COOKIE"):
                response.delete_cookie(settings.JWT_AUTH_REFRESH_COOKIE)

            return response

        except (TokenError, InvalidToken):
            return Response(
                {"message": "Successfully logged out"}, status=status.HTTP_200_OK
            )


class UserProfileView(APIView):
    """User profile endpoint"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Get current user profile",
        responses={200: UserProfileSerializer},
    )
    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Update current user profile",
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer},
    )
    def patch(self, request):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """Change password endpoint"""

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Change user password",
        request_body=ChangePasswordSerializer,
        responses={200: "Password updated successfully"},
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response(
                {"message": "Password updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    """Custom token refresh view that handles cookies"""

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Refresh access token",
        responses={200: TokenSerializer},
    )
    def post(self, request, *args, **kwargs):
        # Try to get refresh token from cookies if not in request data
        if not request.data.get("refresh") and hasattr(
            settings, "JWT_AUTH_REFRESH_COOKIE"
        ):
            refresh_token = request.COOKIES.get(settings.JWT_AUTH_REFRESH_COOKIE)
            if refresh_token:
                # Create a mutable copy of request.data
                request.data._mutable = True
                request.data["refresh"] = refresh_token
                request.data._mutable = False

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200 and hasattr(settings, "JWT_AUTH_COOKIE"):
            access_token = response.data.get("access")
            if access_token:
                response.set_cookie(
                    settings.JWT_AUTH_COOKIE,
                    access_token,
                    max_age=settings.SIMPLE_JWT[
                        "ACCESS_TOKEN_LIFETIME"
                    ].total_seconds(),
                    httponly=settings.JWT_AUTH_COOKIE_HTTP_ONLY,
                    secure=settings.JWT_AUTH_COOKIE_SECURE,
                    samesite=settings.JWT_AUTH_COOKIE_SAMESITE,
                )

        return response
