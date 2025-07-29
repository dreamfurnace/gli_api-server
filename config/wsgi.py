"""
WSGI config for api_admin_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# DJANGO_ENV 확인 및 출력 (설정 로직은 settings.py에서 분기 처리)
env = os.getenv("DJANGO_ENV", "development")
print(f"[wsgi.py] 환경 변수 DJANGO_ENV: {env}", file=sys.stderr)

# settings.py 하나로 통합했으므로 항상 동일한 settings 사용
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
print("[wsgi.py] DJANGO_SETTINGS_MODULE: config.settings", file=sys.stderr)

application = get_wsgi_application()
