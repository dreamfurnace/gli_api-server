import os
from pathlib import Path
from datetime import timedelta
import sys

from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)

print("[settings.py] 로드됨", file=sys.stderr)

# 환경 변수 로드
load_dotenv()
ENV = os.getenv('DJANGO_ENV', 'development')

# env_file = f'.env.{ENV}'
# load_dotenv(env_file)
load_dotenv(f'.env.{ENV}', override=True)
print("[settings.py] 로드된 환경 변수 ~~mT.Tm~~ 고오!!! :", ENV)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Docker 빌드 시에는 더미 값 사용, 런타임에는 실제 값 필요
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    # 빌드 타임에는 더미 값 사용 (실제로는 런타임에 env로 주입됨)
    if os.getenv("DOCKER_BUILD", "false") == "true":
        SECRET_KEY = "docker-build-temporary-secret-key-will-be-replaced-at-runtime"
        print("[settings.py] ⚠️  Using temporary SECRET_KEY for Docker build", file=sys.stderr)
    else:
        raise ValueError("환경변수 DJANGO_SECRET_KEY가 설정되지 않았습니다.")


allowed_hosts = os.getenv("DJANGO_ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [a.strip() for a in allowed_hosts.split(",") if a]

if ENV == "staging":
    DEBUG = False
    ALLOWED_HOSTS += [
        "localhost",
        "127.0.0.1",
        "stg-api.glibiz.com",  # Staging API 도메인
        "gli-staging-alb-461879350.ap-northeast-2.elb.amazonaws.com",  # ALB DNS
        ".elasticbeanstalk.com",
        ".amazonaws.com",
        "*",  # ALB health check를 위해 모든 호스트 허용 (staging only)
        ]
elif ENV == "production":
    DEBUG = False
    ALLOWED_HOSTS += [
        "localhost", 
        "127.0.0.1", 
        "172.31.6.131",  # EC2 내부 접근 IP
        ".elasticbeanstalk.com", 
        ".amazonaws.com"
        ]
else:
    DEBUG = True
    ALLOWED_HOSTS += [
        "0.0.0.0",
        "localhost",
        "127.0.0.1",
        ]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    # Local apps
    "apps.common",
    "apps.solana_auth",
    "apps.gli_content",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ????
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# Custom User Model
AUTH_USER_MODEL = "solana_auth.SolanaUser"

# JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

# API Documentation settings
SPECTACULAR_SETTINGS = {
    "TITLE": "GLI Backend API",
    "DESCRIPTION": "GLI project backend API",
    "VERSION": "1.0.0",
}

# CORS 설정 - 환경별 구성
cors_origins = os.getenv("CORS_ALLOWED_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins.split(",") if origin]

# 환경별 추가 CORS 설정
if ENV == "development":
    # 개발 환경에서는 모든 localhost 포트 허용
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS += [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ]
elif ENV == "staging":
    # 스테이징 환경에서는 제한적 허용
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS += [
        "http://localhost:5173",
        "https://staging-gli-frontend.com",
    ]
elif ENV == "production":
    # 프로덕션 환경에서는 엄격한 제한
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS += [
        "https://gli-user-frontend.com",
        "https://gli-admin-frontend.com",
    ]

# CORS 공통 설정
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-csrf-token',  # 프론트엔드가 사용하는 대시 포함 버전
    'x-requested-with',
    'x-client-version',  # 프론트엔드 클라이언트 버전 헤더
]

print(f"✅ CORS 설정 ({ENV}): ALLOW_ALL={CORS_ALLOW_ALL_ORIGINS}, ORIGINS={CORS_ALLOWED_ORIGINS}", file=sys.stderr)

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database settings
if ENV == "development":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv('DATABASE_NAME'),
            "USER": os.getenv('DATABASE_USER'),
            "PASSWORD": os.getenv('DATABASE_PASSWORD'),
            "HOST": os.getenv('DATABASE_HOST'),
            "PORT": os.getenv('DATABASE_PORT'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

# Static files
# 웹 브라우저가 정적 파일을 접근할 때 쓰는 URL prefix
STATIC_URL = "/static/"
# collectstatic 명령으로 모은 정적 파일들이 저장되는 실제 경로
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# ????
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 개발 중 여러 정적 디렉토리를 수동 등록할 때 사용
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# 환경에 따라 추가 로깅 설정
if ENV in ["staging", "production"]:
    try:
        import os
        # 로그 디렉토리 확인 및 생성
        log_dir = '/var/app/current/logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # 파일 핸들러 추가
        LOGGING['handlers']['file'] = {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_dir, 'django_debug.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 5,
            'formatter': 'verbose',
        }
        LOGGING['formatters'] = {
            'verbose': {
                    'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                    'style': '{',
            },
        }
        LOGGING['loggers']['django']['handlers'].append('file')
    except Exception as e:
        print(f"로그 디렉토리 생성 오류: {e}", file=sys.stderr)


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_S3_REGION', 'ap-northeast-2') # 추가 필요!
AWS_S3_REGION = os.getenv('AWS_S3_REGION', 'ap-northeast-2')  # 필요시

# 미디어(업로드) 파일 경로 설정
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')