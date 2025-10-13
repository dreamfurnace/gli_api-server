from django.urls import path
from . import views
from . import views_face_verification

app_name = 'solana_auth'

urlpatterns = [
    # 인증 엔드포인트
    path('api/auth/login/', views.login, name='login'),
    path('api/auth/nonce/', views.request_nonce, name='request_nonce'),
    path('api/auth/verify/', views.verify_signature, name='verify_signature'),
    path('api/auth/logout/', views.logout, name='logout'),
    path('api/auth/refresh/', views.refresh_token, name='refresh_token'),

    # 사용자 프로필
    path('api/user/profile/', views.user_profile, name='user_profile'),
    path('api/user/transactions/', views.user_transactions, name='user_transactions'),

    # 얼굴 인증
    path('api/users/<str:user_id>/face-verification/', views_face_verification.submit_face_verification, name='submit_face_verification'),
    path('api/users/<str:user_id>/face-verification/status/', views_face_verification.get_face_verification_status, name='face_verification_status'),
    path('api/users/<str:user_id>/face-verification/history/', views_face_verification.get_face_verification_history, name='face_verification_history'),

    # 회원 관리 (Member Management)
    path('api/members/', views.member_list, name='member_list'),
    path('api/members/<uuid:member_id>/', views.member_detail, name='member_detail'),

    # 관리자 관리 (Admin Management)
    path('api/auth/admins/', views.admin_list, name='admin_list'),
    path('api/auth/admins/<int:admin_id>/', views.admin_detail, name='admin_detail'),

    # 대시보드 통계 (Dashboard Statistics)
    path('api/admin/platform-statistics/', views.platform_statistics, name='platform_statistics'),

    # S3 파일 업로드
    path('api/upload/image/', views.upload_image, name='upload_image'),
    path('api/upload/image/delete/', views.delete_image, name='delete_image'),

    # 팀 구성원 관리
    path('api/team-members/', views.team_member_list, name='team_member_list'),
    path('api/team-members/<uuid:member_id>/', views.team_member_detail, name='team_member_detail'),

    # 프로젝트 특징 관리
    path('api/project-features/', views.project_feature_list, name='project_feature_list'),
    path('api/project-features/<uuid:feature_id>/', views.project_feature_detail, name='project_feature_detail'),

    # 전략 로드맵 관리
    path('api/strategy-phases/', views.strategy_phase_list, name='strategy_phase_list'),
    path('api/strategy-phases/<uuid:phase_id>/', views.strategy_phase_detail, name='strategy_phase_detail'),

    # 개발 일정 관리
    path('api/development-timelines/', views.development_timeline_list, name='development_timeline_list'),
    path('api/development-timelines/<uuid:timeline_id>/', views.development_timeline_detail, name='development_timeline_detail'),

    # 토큰 에코시스템 관리
    path('api/token-ecosystems/', views.token_ecosystem_list, name='token_ecosystem_list'),
    path('api/token-ecosystems/<uuid:token_id>/', views.token_ecosystem_detail, name='token_ecosystem_detail'),
]