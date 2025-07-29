#!/bin/bash
set -e

# Activate virtual environment
source /var/app/venv/*/bin/activate

# Navigate to application directory
cd /var/app/current

# Auto-detect DJANGO_ENV from existing file
if [ -f ".env.production" ]; then
  export DJANGO_ENV=production
  ENV_FILE=".env.production"
elif [ -f ".env.staging" ]; then
  export DJANGO_ENV=staging
  ENV_FILE=".env.staging"
else
  export DJANGO_ENV=development
  ENV_FILE=".env.development"
fi
echo "[eb_run.sh] Using DJANGO_ENV=${DJANGO_ENV}"

# Load env vars
if [ -f "$ENV_FILE" ]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Django 관리 명령어 실행
# Run DB migrations
echo "[eb_run.sh] Running migrate..."
python manage.py migrate --noinput

# Collect static files
echo "[eb_run.sh] Collecting static files..."
python manage.py collectstatic --noinput

echo "[eb_run.sh] Loading initial data..."
python manage.py loaddata initial_data.json || echo "[eb_run.sh] loaddata failed, ignoring"

echo "[eb_run.sh] Running setup_admins..."
python manage.py setup_admins || echo "[eb_run.sh] setup_admins failed, ignoring"

# Ensure logs directory exists
mkdir -p logs

# Start Gunicorn
gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --access-logfile=logs/gunicorn-access.log \
    --error-logfile=logs/gunicorn-error.log
