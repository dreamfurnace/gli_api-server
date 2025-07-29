#!/bin/bash
# 📦 run.sh: 로컬 개발 및 수동 운영을 위한 Django/Celery 실행 스크립트
# 실행 방법:
#   ./run.sh dev:server     → 개발 서버 실행
#   ./run.sh dev:worker     → 개발용 Celery 워커 실행
#   ./run.sh stage:worker   → 스테이징 Celery 워커 실행
#   ./run.sh prod:server    → 프로덕션 gunicorn 실행

set -e

# 환경 변수 ENV 에 아무 값도 없으면 development 로 설정
if [[ -z "$ENV" ]]; then
  ENV="development"
fi

ENV_FILE=".env.$ENV"
if [[ -f "$ENV_FILE" ]]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
else
  echo "❌ 환경파일 $ENV_FILE 이 없습니다."
  exit 1
fi


# 파라미터 검사
if [[ -z "$1" ]]; then
  echo "Usage: $0 {dev:server|dev:worker|stage:server|stage:worker|prod:server|prod:worker}"
  exit 1
fi

# env:role 형태 파싱
MODE="$1"
ENV="${MODE%%:*}"   # 앞부분 → dev, stage, prod
ROLE="${MODE##*:}"  # 뒷부분 → server, worker

export DJANGO_ENV="$ENV"
echo "[${DJANGO_ENV}] Running: $ROLE" | sed 's/\(.*\)/[\U\1]/'

# 역할별 실행
case "$ROLE" in
  server)
    if [[ "$ENV" == "prod" ]]; then
      echo "[PROD] Starting prod ENV gunicorn...: $ENV"
      uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000
    elif [[ "$ENV" == "stage" ]]; then
      echo "[STAGE] Starting stage ENV gunicorn...: $ENV"
      uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2
    elif [[ "$ENV" == "dev" ]]; then
      echo "[DEV] Starting dev ENV Django dev server...: $ENV"
      uv run python manage.py runserver
    fi
    ;;
  worker)
    echo "Starting Celery worker..."
    # celery -A config worker --loglevel=info
    uv run celery -A config worker --loglevel=info
    ;;
  *)
    echo "Unknown role: $ROLE"
    exit 1
    ;;
esac
