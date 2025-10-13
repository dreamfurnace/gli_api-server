from rest_framework import permissions
from apps.solana_auth.models import AdminUser


class IsSuperAdmin(permissions.BasePermission):
    """
    슈퍼 관리자 권한 체크
    SolanaUser와 AdminUser 모델을 모두 확인하여 일관성 확보
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # 1단계: SolanaUser 기본 권한 확인
        if not request.user.is_active:
            return False

        if not request.user.is_staff:
            return False

        # 2단계: AdminUser 확장 권한 확인
        try:
            admin_user = AdminUser.objects.select_related('grade').get(user=request.user)

            # AdminUser 활성화 상태 확인
            if not admin_user.is_active:
                return False

            # 슈퍼 관리자 등급 확인
            return admin_user.grade.name == "슈퍼 관리자"

        except AdminUser.DoesNotExist:
            # AdminUser가 없어도 SolanaUser가 슈퍼유저면 허용
            return request.user.is_superuser


class IsAdmin(permissions.BasePermission):
    """
    일반 관리자 권한 체크
    SolanaUser와 AdminUser 모두 확인
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # 1단계: SolanaUser 기본 권한 확인
        if not request.user.is_active:
            return False

        if not request.user.is_staff:
            return False

        # 2단계: AdminUser 확장 권한 확인
        try:
            admin_user = AdminUser.objects.select_related('grade').get(user=request.user)
            return admin_user.is_active
        except AdminUser.DoesNotExist:
            # AdminUser가 없어도 SolanaUser가 슈퍼유저면 허용
            return request.user.is_superuser


class IsActiveAdmin(permissions.BasePermission):
    """
    활성화된 관리자 권한 체크
    SolanaUser와 AdminUser 모두 활성화된 상태인지 확인
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # SolanaUser 활성화 확인
        if not request.user.is_active:
            return False

        # SolanaUser 관리자 권한 확인
        if not request.user.is_staff:
            return False

        # AdminUser 활성화 확인
        try:
            admin_user = AdminUser.objects.get(user=request.user)
            return admin_user.is_active
        except AdminUser.DoesNotExist:
            # AdminUser가 없어도 SolanaUser가 슈퍼유저면 허용
            return request.user.is_superuser
