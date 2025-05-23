import logging

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

logger = logging.getLogger(__name__)


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication class that handles both cookie and header-based authentication
    """

    def authenticate(self, request):
        """
        Attempts to authenticate using cookies first, then falls back to header-based authentication.
        """
        try:
            # Try to authenticate with the Authorization header first
            header_auth = self.get_header(request)
            if header_auth:
                raw_token = self.get_raw_token(header_auth)
                if raw_token:
                    return self.process_token(raw_token, request)

            # Try to authenticate with cookies
            cookie_name = settings.JWT_AUTH_COOKIE
            if cookie_name and cookie_name in request.COOKIES:
                raw_token = request.COOKIES.get(cookie_name)
                if raw_token:
                    return self.process_token(raw_token, request)

            # If no successful authentication, return None to indicate no authentication occurred
            logger.info("No JWT token found in header or cookie")
            return None

        except (InvalidToken, AuthenticationFailed) as e:
            logger.error(f"Authentication error: {type(e).__name__} - {str(e)}")
            return None

        # If no successful authentication, return None to indicate no authentication occurred

    def process_token(self, raw_token, request):
        """
        Process the token and return the user and validated token
        """
        if settings.DEBUG and logger.isEnabledFor(logging.DEBUG):
            logger.debug("Attempting to authenticate with token: %s", raw_token)

        try:
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
        except Exception as e:
            logger.error(f"Error processing token: {type(e).__name__} - {str(e)}")
            raise AuthenticationFailed(_("Invalid token"))
