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
    python manage.py createsuperuser --noinput || true
fi

# Collect static files in production
if [ "$1" = "gunicorn" ]; then
    echo "📦 Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Start server
echo "🌐 Starting server..."
if [ "$1" = "runserver" ]; then
    exec python manage.py runserver 0.0.0.0:8000
elif [ "$1" = "gunicorn" ]; then
    # Workers are separate processes that handle incoming requests in parallel
    # The optimal number of workers depends on your server's CPU cores
    # Formula: (2 × CPU cores) + 1
    # For example, on a 2-core server, 5 workers would be optimal
    # Adjust based on your production server's resources
    exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers $(( 2 * $(nproc) + 1 ))
else
    exec "$@"
fi 