#!/bin/bash
set -e

echo "🗄️ Running database migrations..."
python manage.py migrate --noinput || {
  echo "⚠️ Migration failed, retrying once with --run-syncdb...";
  python manage.py migrate --run-syncdb --noinput || true;
}

echo "🚀 Starting Gunicorn..."
exec gunicorn CryptoQWeb.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120


