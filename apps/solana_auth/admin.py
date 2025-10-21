from django.contrib import admin
from .models import SolanaUser, AuthNonce, SolanaTransaction, FaceVerification, AdminGrade, AdminUser, AdminPermission, GradePermission, TeamMember, ProjectFeature, StrategyPhase


@admin.register(SolanaUser)
class SolanaUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'wallet_address', 'membership_level', 'sol_balance', 'is_active', 'created_at']
    list_filter = ['membership_level', 'is_active', 'created_at']
    search_fields = ['username', 'wallet_address', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_login', 'last_balance_update']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('wallet_address', 'username', 'email', 'first_name', 'last_name')
        }),
        ('GLI Platform 정보', {
            'fields': ('membership_level', 'sol_balance', 'last_balance_update')
        }),
        ('계정 관리', {
            'fields': ('is_active', 'created_at', 'updated_at', 'last_login')
        }),
    )


@admin.register(AuthNonce)
class AuthNonceAdmin(admin.ModelAdmin):
    list_display = ['wallet_address', 'nonce', 'is_consumed', 'created_at']
    list_filter = ['is_consumed', 'created_at']
    search_fields = ['wallet_address', 'nonce']
    readonly_fields = ['created_at']


@admin.register(SolanaTransaction)
class SolanaTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'amount', 'status', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['user__username', 'user__wallet_address', 'transaction_hash']
    readonly_fields = ['created_at', 'confirmed_at']

    fieldsets = (
        ('트랜잭션 정보', {
            'fields': ('user', 'transaction_hash', 'transaction_type', 'amount')
        }),
        ('상태 관리', {
            'fields': ('status', 'created_at', 'confirmed_at')
        }),
    )


@admin.register(FaceVerification)
class FaceVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'verified', 'confidence', 'liveness_score', 'attempts', 'verification_timestamp', 'created_at']
    list_filter = ['verified', 'created_at', 'verification_timestamp']
    search_fields = ['user__username', 'user__wallet_address', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        ('사용자 정보', {
            'fields': ('id', 'user')
        }),
        ('인증 결과', {
            'fields': ('verified', 'confidence', 'liveness_score', 'attempts')
        }),
        ('상세 정보', {
            'fields': ('check_details',),
            'classes': ('collapse',)
        }),
        ('타임스탬프', {
            'fields': ('verification_timestamp', 'created_at', 'updated_at')
        }),
    )

    def get_queryset(self, request):
        """최적화를 위해 user를 미리 로드"""
        qs = super().get_queryset(request)
        return qs.select_related('user')


# ============================================================================
# 관리자 관리 모델 Admin (Admin Management Models)
# ============================================================================

@admin.register(AdminGrade)
class AdminGradeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'grade', 'is_active', 'last_login_ip', 'created_at']
    list_filter = ['grade', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'grade')


@admin.register(AdminPermission)
class AdminPermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'codename', 'description', 'created_at']
    search_fields = ['name', 'codename', 'description']
    readonly_fields = ['created_at']


@admin.register(GradePermission)
class GradePermissionAdmin(admin.ModelAdmin):
    list_display = ['grade', 'permission', 'created_at']
    list_filter = ['grade', 'created_at']
    search_fields = ['grade__name', 'permission__name']
    readonly_fields = ['created_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('grade', 'permission')


# ============================================================================
# 팀 구성원 모델 Admin (Team Member Models)
# ============================================================================

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['position_ko', 'position_en', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['position_ko', 'position_en', 'role_ko', 'role_en']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['order', '-created_at']

    fieldsets = (
        ('기본 정보', {
            'fields': ('id', 'image_url')
        }),
        ('직책 정보', {
            'fields': ('position_ko', 'position_en', 'role_ko', 'role_en')
        }),
        ('태그 및 표시 설정', {
            'fields': ('tags', 'order', 'is_active')
        }),
        ('타임스탬프', {
            'fields': ('created_at', 'updated_at')
        }),
    )


# ============================================================================
# 프로젝트 소개 모델 Admin (Project Feature Models)
# ============================================================================

@admin.register(ProjectFeature)
class ProjectFeatureAdmin(admin.ModelAdmin):
    list_display = ['icon', 'title_ko', 'title_en', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title_ko', 'title_en', 'description_ko', 'description_en']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['order', '-created_at']

    fieldsets = (
        ('기본 정보', {
            'fields': ('id', 'icon')
        }),
        ('제목 및 설명', {
            'fields': ('title_ko', 'title_en', 'description_ko', 'description_en')
        }),
        ('표시 설정', {
            'fields': ('order', 'is_active')
        }),
        ('타임스탬프', {
            'fields': ('created_at', 'updated_at')
        }),
    )


# ============================================================================
# 전략 로드맵 모델 Admin (Strategy Roadmap Models)
# ============================================================================

@admin.register(StrategyPhase)
class StrategyPhaseAdmin(admin.ModelAdmin):
    list_display = ['icon', 'title_ko', 'title_en', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title_ko', 'title_en', 'description_ko', 'description_en']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['order', '-created_at']

    fieldsets = (
        ('기본 정보', {
            'fields': ('id', 'icon')
        }),
        ('제목 및 설명', {
            'fields': ('title_ko', 'title_en', 'description_ko', 'description_en')
        }),
        ('주요 기능', {
            'fields': ('features',)
        }),
        ('표시 설정', {
            'fields': ('order', 'is_active')
        }),
        ('타임스탬프', {
            'fields': ('created_at', 'updated_at')
        }),
    )