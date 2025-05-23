from django.urls import path

from apps.authentication.views import (
    ChangePasswordView,
    CustomTokenRefreshView,
    LoginView,
    LogoutView,
    RegisterView,
    UserProfileView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
