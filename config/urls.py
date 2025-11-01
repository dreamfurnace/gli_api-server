# config/urls.py
import os
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

ENV = os.getenv("DJANGO_ENV", "development")
# print(f"[wsgi.py] 환경 변수 DJANGO_ENV: {ENV}", file=sys.stderr)

admin.site.site_header = f"GLI Admin - ENV:{ENV}"
admin.site.site_title = f"GLI Admin-{ENV}"
admin.site.index_title = "GLI 관리자 대시보드"

def root_ok(request):
    return JsonResponse({"message": "Django is alive!", "env": ENV})
def health_check(request):
    # return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "ok", "env": ENV})

urlpatterns = [
    path("", root_ok),
    # EB에서 Health Check URL
    path("health/", health_check),

    # Admin URLs
    path('admin/', admin.site.urls),

    # API Documentation URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='api-docs'),  # /api/docs 별칭 추가
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Common URLs
    path('api/common/', include('apps.common.urls')),

    # Solana Auth URLs
    path('', include('apps.solana_auth.urls')),

    # GLI Content Management URLs
    path('', include('apps.gli_content.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)