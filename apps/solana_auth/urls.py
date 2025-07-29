from django.urls import path
from . import views

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
]