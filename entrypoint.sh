#!/bin/sh
set -e

echo "🎯 Running migrations..."
python /app/src/manage.py migrate --noinput

echo "📦 Collecting static files..."
python /app/src/manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8080 --log-level info