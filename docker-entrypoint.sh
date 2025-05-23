#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

echo "🚀 Starting container..."

# Wait for PostgreSQL
postgres_ready() {
    python << END
import sys
import psycopg2
try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(1)
sys.exit(0)
END
}

echo "⏳ Waiting for PostgreSQL..."
until postgres_ready; do
  echo "PostgreSQL unavailable - sleeping"
  sleep 1
done
echo "✅ PostgreSQL is available"

# Apply database migrations
echo "🔄 Applying database migrations..."
python manage.py migrate

# Create superuser if needed (in development)
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    echo "👤 Creating/updating superuser..."
    echo "Debug: DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-'not set'}"
    echo "Debug: DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-'not set'}"
    
    # Check if superuser already exists
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
username = '${DJANGO_SUPERUSER_USERNAME}'
if User.objects.filter(username=username).exists():
    print(f'Superuser {username} already exists')
else:
    try:
        User.objects.create_superuser(
            username='${DJANGO_SUPERUSER_USERNAME}',
            email='${DJANGO_SUPERUSER_EMAIL}',
            password='${DJANGO_SUPERUSER_PASSWORD}'
        )
        print(f'Superuser {username} created successfully')
    except Exception as e:
        print(f'Error creating superuser: {e}')
        exit(1)
" || echo "Failed to create superuser, continuing..."
fi

# Get the first argument (default to empty string if not provided)
COMMAND="${1:-}"

# Collect static files in production
if [ "$COMMAND" = "gunicorn" ]; then
    echo "📦 Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Start server
echo "🌐 Starting server..."
if [ "$COMMAND" = "runserver" ]; then
    exec python manage.py runserver 0.0.0.0:8000
elif [ "$COMMAND" = "gunicorn" ]; then
    # Workers are separate processes that handle incoming requests in parallel
    # The optimal number of workers depends on your server's CPU cores
    # Formula: (2 × CPU cores) + 1
    # For example, on a 2-core server, 5 workers would be optimal
    # Adjust based on your production server's resources
    exec gunicorn core.asgi:application --bind 0.0.0.0:8000 --workers $(( 2 * $(nproc) + 1 ))
elif [ -n "$COMMAND" ]; then
    exec "$@"
else
    echo "No command specified. Available commands: runserver, gunicorn"
    echo "Starting development server by default..."
    exec python manage.py runserver 0.0.0.0:8000
fi 