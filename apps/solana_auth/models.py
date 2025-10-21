from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import uuid


class SolanaUser(AbstractUser):
    """Solana 지갑 기반 사용자 모델"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet_address = models.CharField(max_length=50, unique=True, db_index=True, blank=True, null=True)

    # AbstractUser의 기본 필드들을 오버라이드
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    # Django 인증 시스템 호환성을 위한 설정
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # wallet_address를 필수 필드에서 제거

    # GLI Platform 관련 필드
    membership_level = models.CharField(
        max_length=20,
        choices=[
            ('basic', 'Basic GLI Member'),
            ('premium', 'Premium GLI Member'),
            ('vip', 'VIP GLI Member')
        ],
        default='premium'
    )

    # 솔라나 관련 정보
    sol_balance = models.DecimalField(max_digits=20, decimal_places=9, default=0)
    last_balance_update = models.DateTimeField(auto_now=True)

    # VPX 등급 시스템 (비트플래그 기반)
    vpx_verify = models.IntegerField(
        default=1,
        help_text='V(Verify) 포인트: 1=이메일인증, 2=핸드폰인증, 4=3D얼굴인증 (비트플래그, 최대 7)'
    )
    vpx_partner = models.IntegerField(
        default=0,
        help_text='P(Partner) 포인트: 1=GLID확보, 2=GLID예치, 4=GLIB엔젤&프리세일 (비트플래그, 최대 7)'
    )
    vpx_experience = models.IntegerField(
        default=0,
        help_text='X(eXperience) 포인트: 1=웹3월렛연동, 2=GLIL사용, 4=GLIB사용 (비트플래그, 최대 7)'
    )

    # 계정 관리
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'solana_users'
        ordering = ['-created_at']

    def __str__(self):
        if self.wallet_address:
            return f"{self.username or 'GLI Member'} ({self.wallet_address[:8]}...)"
        else:
            return f"{self.username or 'GLI Member'} (No Wallet)"


class AuthNonce(models.Model):
    """인증용 nonce 관리"""
    wallet_address = models.CharField(max_length=50, db_index=True)
    nonce = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    class Meta:
        db_table = 'auth_nonces'
        ordering = ['-created_at']

    def __str__(self):
        return f"Nonce for {self.wallet_address[:8]}... ({'used' if self.used else 'active'})"


class SolanaTransaction(models.Model):
    """솔라나 트랜잭션 기록"""
    user = models.ForeignKey(SolanaUser, on_delete=models.CASCADE, related_name='transactions')
    transaction_hash = models.CharField(max_length=100, unique=True)
    transaction_type = models.CharField(
        max_length=20,
        choices=[
            ('airdrop', 'Airdrop'),
            ('transfer', 'Transfer'),
            ('mint', 'NFT Mint'),
            ('stake', 'Staking'),
            ('reward', 'Reward')
        ]
    )
    amount = models.DecimalField(max_digits=20, decimal_places=9, default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('failed', 'Failed')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'solana_transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} SOL ({self.status})"


class FaceVerification(models.Model):
    """얼굴 인증 기록"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        SolanaUser,
        on_delete=models.CASCADE,
        related_name='face_verifications'
    )

    # 인증 결과
    verified = models.BooleanField(
        default=False,
        help_text='얼굴 인증 성공 여부'
    )
    confidence = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        help_text='인증 신뢰도 (0.0 ~ 1.0)'
    )
    liveness_score = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        help_text='생체 확인 점수 (0.0 ~ 1.0)'
    )

    # 인증 시도 정보
    attempts = models.IntegerField(
        default=1,
        help_text='인증 시도 횟수'
    )

    # 상세 체크 결과 (JSON 형식)
    check_details = models.JSONField(
        blank=True,
        null=True,
        help_text='단계별 인증 상세 정보 (눈 깜박임, 고개 돌림 등)'
    )

    # 타임스탬프
    verification_timestamp = models.DateTimeField(
        help_text='프론트엔드에서 전송한 인증 시각'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'face_verifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['verified', '-created_at']),
        ]

    def __str__(self):
        status = '✅ 성공' if self.verified else '❌ 실패'
        return f"{self.user.username} - {status} ({self.confidence})"


# ============================================================================
# 관리자 관리 모델 (Admin Management Models)
# ============================================================================

class AdminGrade(models.Model):
    """관리자 등급 정의"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_grades'

    def __str__(self):
        return self.name


class AdminUser(models.Model):
    """관리자 사용자 확장 정보"""
    user = models.OneToOneField(SolanaUser, on_delete=models.CASCADE, related_name='admin_profile')
    grade = models.ForeignKey(AdminGrade, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_users'

    def clean(self):
        if not self.user.is_staff:
            raise ValidationError("Admin user must have staff status")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.grade.name})"


class AdminPermission(models.Model):
    """관리자 권한 정의"""
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_permissions'

    def __str__(self):
        return self.name


class GradePermission(models.Model):
    """등급별 권한 매핑"""
    grade = models.ForeignKey(AdminGrade, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(AdminPermission, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'grade_permissions'
        unique_together = ('grade', 'permission')

    def __str__(self):
        return f"{self.grade.name} - {self.permission.name}"


# ============================================================================
# 팀 구성원 모델 (Team Member Models)
# ============================================================================

class TeamMember(models.Model):
    """팀 구성원 정보"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 기본 정보
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='팀원 사진 URL (S3) - 선택사항'
    )

    # 이름 (한글/영문)
    name_ko = models.CharField(
        max_length=50,
        default='미입력',
        help_text='이름 (한글) 예: 김GLI'
    )
    name_en = models.CharField(
        max_length=50,
        default='Not Entered',
        help_text='이름 (영문) 예: GLI Kim'
    )

    # 직책 (한글/영문)
    position_ko = models.CharField(
        max_length=100,
        help_text='직책 (한글) 예: GLI CEO'
    )
    position_en = models.CharField(
        max_length=100,
        help_text='직책 (영문) 예: Chief Executive Officer'
    )

    # 역할 설명 (한글/영문)
    role_ko = models.TextField(
        help_text='역할 설명 (한글) 예: 블록체인 비즈니스 전략 및 전반적인 경영을 담당합니다.'
    )
    role_en = models.TextField(
        help_text='역할 설명 (영문) 예: Responsible for blockchain business strategy and overall management.'
    )

    # 태그 (JSON 배열)
    tags = models.JSONField(
        default=list,
        help_text='기술 태그 배열 예: ["Blockchain", "Business Strategy", "Leadership"]'
    )

    # 정렬 및 표시 제어
    order = models.IntegerField(
        default=0,
        help_text='표시 순서 (낮을수록 먼저 표시)'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='팀원 표시 여부'
    )

    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'team_members'
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['order', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name_ko} ({self.position_ko}) - {self.order}"


# ============================================================================
# 프로젝트 소개 모델 (Project Feature Models)
# ============================================================================

class ProjectFeature(models.Model):
    """프로젝트 소개 특징"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 아이콘
    icon = models.CharField(
        max_length=10,
        help_text='아이콘 emoji 예: 🌊'
    )

    # 제목 (한글/영문)
    title_ko = models.CharField(
        max_length=200,
        help_text='제목 (한글) 예: 비전'
    )
    title_en = models.CharField(
        max_length=200,
        help_text='제목 (영문) 예: Vision'
    )

    # 설명 (한글/영문)
    description_ko = models.TextField(
        help_text='설명 (한글)'
    )
    description_en = models.TextField(
        help_text='설명 (영문)'
    )

    # 정렬 및 표시 제어
    order = models.IntegerField(
        default=0,
        help_text='표시 순서 (낮을수록 먼저 표시)'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='특징 표시 여부'
    )

    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_features'
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['order', 'is_active']),
        ]

    def __str__(self):
        return f"{self.icon} {self.title_ko} - {self.order}"


# ============================================================================
# 전략 로드맵 모델 (Strategy Roadmap Models)
# ============================================================================

class StrategyPhase(models.Model):
    """전략 로드맵 페이즈"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 아이콘
    icon = models.CharField(
        max_length=10,
        help_text='아이콘 emoji 예: 🚀'
    )

    # 제목 (한글/영문)
    title_ko = models.CharField(
        max_length=200,
        help_text='제목 (한글) 예: 플랫폼 구축'
    )
    title_en = models.CharField(
        max_length=200,
        help_text='제목 (영문) 예: Platform Development'
    )

    # 설명 (한글/영문)
    description_ko = models.TextField(
        help_text='설명 (한글)'
    )
    description_en = models.TextField(
        help_text='설명 (영문)'
    )

    # 주요 기능 (JSON 배열 - 한글/영문)
    features_ko = models.JSONField(
        default=list,
        help_text='주요 기능 목록 (한글) JSON 배열 예: ["웹 플랫폼 개발", "GLIB/GLID/GLIL 토큰 발행", "지갑 연동 시스템"]'
    )
    features_en = models.JSONField(
        default=list,
        help_text='주요 기능 목록 (영문) JSON 배열 예: ["Web platform development", "GLIB/GLID/GLIL token issuance", "Wallet integration system"]'
    )

    # 정렬 및 표시 제어
    order = models.IntegerField(
        default=0,
        help_text='표시 순서 (낮을수록 먼저 표시)'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='페이즈 표시 여부'
    )

    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'strategy_phases'
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['order', 'is_active']),
        ]

    def __str__(self):
        return f"{self.icon} {self.title_ko} - {self.order}"


# ============================================================================
# 개발 일정 관리 모델 (Development Timeline Models)
# ============================================================================

class DevelopmentTimeline(models.Model):
    """개발 일정 관리"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 분기
    quarter = models.CharField(
        max_length=20,
        help_text='분기 정보 예: 2024 Q1'
    )

    # 상태 아이콘
    status_icon = models.CharField(
        max_length=10,
        help_text='상태 아이콘 예: ✅ (완료), 🔄 (진행중), ⏳ (대기)'
    )

    # 제목 (한글/영문)
    title_ko = models.CharField(
        max_length=200,
        help_text='제목 (한글) 예: 플랫폼 MVP 출시'
    )
    title_en = models.CharField(
        max_length=200,
        help_text='제목 (영문) 예: Platform MVP Launch'
    )

    # 설명 (한글/영문)
    description_ko = models.TextField(
        help_text='설명 (한글)'
    )
    description_en = models.TextField(
        help_text='설명 (영문)'
    )

    # 정렬 및 표시 제어
    order = models.IntegerField(
        default=0,
        help_text='표시 순서 (낮을수록 먼저 표시)'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='일정 표시 여부'
    )

    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'development_timelines'
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['order', 'is_active']),
        ]

    def __str__(self):
        return f"{self.quarter} {self.status_icon} {self.title_ko}"


# ============================================================================
# 토큰 에코시스템 모델 (Token Ecosystem Models)
# ============================================================================

class TokenEcosystem(models.Model):
    """토큰 에코시스템 정보"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 아이콘
    icon = models.CharField(
        max_length=10,
        help_text='아이콘 emoji 예: 🔵'
    )

    # 토큰 이름 및 심볼
    name = models.CharField(
        max_length=100,
        help_text='토큰 이름 예: GLI Business'
    )
    symbol = models.CharField(
        max_length=20,
        help_text='토큰 심볼 예: GLIB'
    )

    # 설명 (한글/영문)
    description_ko = models.TextField(
        help_text='설명 (한글)'
    )
    description_en = models.TextField(
        help_text='설명 (영문)'
    )

    # 주요 기능 (JSON 배열 - 한글/영문)
    features_ko = models.JSONField(
        default=list,
        help_text='주요 기능 목록 (한글) JSON 배열 예: ["투표 및 의사 결정 참여", "특별 혜택 및 보상", "플랫폼 성장 수익 공유"]'
    )
    features_en = models.JSONField(
        default=list,
        help_text='주요 기능 목록 (영문) JSON 배열 예: ["Participation in voting and decision-making", "Special benefits and rewards", "Platform growth revenue sharing"]'
    )

    # 토큰 정보
    total_supply = models.CharField(
        max_length=100,
        help_text='총 공급량 예: 100,000,000 GLIB 또는 무제한'
    )
    current_price = models.CharField(
        max_length=50,
        help_text='현재 가격 예: $0.25'
    )

    # 정렬 및 표시 제어
    order = models.IntegerField(
        default=0,
        help_text='표시 순서 (낮을수록 먼저 표시)'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='토큰 표시 여부'
    )

    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'token_ecosystems'
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['order', 'is_active']),
        ]

    def __str__(self):
        return f"{self.icon} {self.name} ({self.symbol})"
