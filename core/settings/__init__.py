import os

# Get the environment from environment variable, default to development
ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "development":
    from .development import *
else:
    from .development import *
