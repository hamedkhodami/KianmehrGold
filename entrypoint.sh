#!/bin/sh
set -e

if [ "${RUN_MIGRATIONS:-0}" = "1" ]; then
    echo "🎯 Running migrations..."
    python /app/src/manage.py migrate --noinput
fi

if [ "${COLLECT_STATIC:-0}" = "1" ]; then
    echo "📦 Collecting static files..."
    python /app/src/manage.py collectstatic --noinput
fi

echo "🚀 Starting: $*"
exec "$@"