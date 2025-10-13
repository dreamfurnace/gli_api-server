# GLI Django API Server Dockerfile
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필수 도구 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# uv 설치
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# 의존성 파일 복사
COPY pyproject.toml uv.lock ./

# uv를 사용하여 의존성 설치
RUN uv sync --frozen

# 애플리케이션 코드 복사
COPY . .

# 정적 파일 수집
RUN uv run python manage.py collectstatic --noinput || true

# 로그 디렉토리 생성
RUN mkdir -p /app/logs

# 포트 노출
EXPOSE 8000

# Gunicorn으로 Django 실행
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "300", "--access-logfile", "-", "--error-logfile", "-", "config.wsgi:application"]
