from rest_framework import serializers
from .models import SolanaUser, AuthNonce, SolanaTransaction, FaceVerification, AdminGrade, AdminUser, AdminPermission, GradePermission, TeamMember, ProjectFeature, StrategyPhase, DevelopmentTimeline, TokenEcosystem, NewsArticle, EmailVerificationCode


class SolanaUserSerializer(serializers.ModelSerializer):
    """솔라나 사용자 시리얼라이저"""
    
    class Meta:
        model = SolanaUser
        fields = [
            'id', 'wallet_address', 'email', 'username',
            'first_name', 'last_name', 'membership_level',
            'sol_balance', 'last_balance_update', 'is_active',
            'vpx_verify', 'vpx_partner', 'vpx_experience',
            'created_at', 'updated_at', 'last_login'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_login']
    
    def to_representation(self, instance):
        """지갑 주소가 없는 경우 처리"""
        data = super().to_representation(instance)
        if not data.get('wallet_address'):
            data['wallet_address'] = None
        return data


class NonceRequestSerializer(serializers.Serializer):
    """Nonce 요청 시리얼라이저"""
    wallet_address = serializers.CharField(max_length=50)
    
    def validate_wallet_address(self, value):
        """지갑 주소 유효성 검증"""
        if not value or len(value) < 32:
            raise serializers.ValidationError("유효하지 않은 지갑 주소입니다.")
        return value


class AuthVerifySerializer(serializers.Serializer):
    """인증 검증 시리얼라이저"""
    wallet_address = serializers.CharField(max_length=50)
    signature = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=255),
        min_length=64,
        max_length=64
    )
    message = serializers.CharField()
    nonce = serializers.CharField(max_length=64)
    
    def validate_wallet_address(self, value):
        """지갑 주소 유효성 검증"""
        if not value or len(value) < 32:
            raise serializers.ValidationError("유효하지 않은 지갑 주소입니다.")
        return value


class SolanaTransactionSerializer(serializers.ModelSerializer):
    """솔라나 트랜잭션 시리얼라이저"""

    class Meta:
        model = SolanaTransaction
        fields = '__all__'
        read_only_fields = ['created_at', 'confirmed_at']


class CheckDetailSerializer(serializers.Serializer):
    """얼굴 인증 체크 상세 정보 시리얼라이저"""
    checkId = serializers.CharField()
    type = serializers.CharField()
    instruction = serializers.CharField()
    passed = serializers.BooleanField()
    score = serializers.FloatField()
    checksPassed = serializers.IntegerField()
    totalChecks = serializers.IntegerField()


class FaceVerificationCreateSerializer(serializers.Serializer):
    """얼굴 인증 결과 생성 시리얼라이저 (POST 요청용)"""
    verified = serializers.BooleanField()
    confidence = serializers.DecimalField(max_digits=5, decimal_places=4)
    livenessScore = serializers.DecimalField(max_digits=5, decimal_places=4, source='liveness_score')
    timestamp = serializers.DateTimeField()
    attempts = serializers.IntegerField(default=1)
    checkDetails = CheckDetailSerializer(many=True, required=False, allow_null=True, source='check_details')

    def validate_confidence(self, value):
        """신뢰도 범위 검증 (0.0 ~ 1.0)"""
        if value < 0 or value > 1:
            raise serializers.ValidationError("신뢰도는 0.0에서 1.0 사이여야 합니다.")
        return value

    def validate_livenessScore(self, value):
        """생체 확인 점수 범위 검증 (0.0 ~ 1.0)"""
        if value < 0 or value > 1:
            raise serializers.ValidationError("생체 확인 점수는 0.0에서 1.0 사이여야 합니다.")
        return value

    def validate_attempts(self, value):
        """시도 횟수 검증"""
        if value < 1:
            raise serializers.ValidationError("시도 횟수는 1 이상이어야 합니다.")
        return value


class FaceVerificationSerializer(serializers.ModelSerializer):
    """얼굴 인증 기록 시리얼라이저 (읽기용)"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_wallet_address = serializers.CharField(source='user.wallet_address', read_only=True)

    class Meta:
        model = FaceVerification
        fields = [
            'id',
            'user',
            'user_username',
            'user_wallet_address',
            'verified',
            'confidence',
            'liveness_score',
            'attempts',
            'check_details',
            'verification_timestamp',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ============================================================================
# 관리자 관리 Serializers (Admin Management Serializers)
# ============================================================================

class AdminPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPermission
        fields = ['id', 'name', 'codename', 'description']


class AdminGradeSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = AdminGrade
        fields = ['id', 'name', 'description', 'permissions']

    def get_permissions(self, obj):
        # 해당 등급의 권한 목록 반환
        permissions = obj.permissions.select_related('permission').all()
        return AdminPermissionSerializer(
            [perm.permission for perm in permissions],
            many=True
        ).data


class AdminUserDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    grade = AdminGradeSerializer()

    class Meta:
        model = AdminUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                 'grade', 'is_active', 'last_login_ip', 'created_at', 'updated_at']


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    grade_id = serializers.IntegerField()

    class Meta:
        model = AdminUser
        fields = ['grade_id', 'is_active']

# ============================================================================
# 팀 구성원 Serializers (Team Member Serializers)
# ============================================================================

class TeamMemberSerializer(serializers.ModelSerializer):
    """팀 구성원 시리얼라이저"""

    class Meta:
        model = TeamMember
        fields = [
            'id', 'image_url', 'name_ko', 'name_en', 'position_ko', 'position_en',
            'role_ko', 'role_en', 'tags', 'order', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'image_url': {'required': False, 'allow_blank': True, 'allow_null': True},
        }

    def validate_image_url(self, value):
        """image_url 필드 검증 - 선택사항"""
        # None이나 빈 문자열은 허용
        if not value:
            return None

        # 배열이 전달된 경우 첫 번째 요소를 사용하거나 에러 처리
        if isinstance(value, list):
            if len(value) > 0 and isinstance(value[0], str):
                return value[0]  # 배열의 첫 번째 요소를 사용
            else:
                raise serializers.ValidationError(
                    "image_url이 배열로 전달되었지만 유효한 URL이 없습니다."
                )

        # URL 형식 검증
        if not isinstance(value, str):
            raise serializers.ValidationError("image_url은 문자열이어야 합니다.")

        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("유효한 URL 형식이 아닙니다.")

        return value

    def validate_tags(self, value):
        """태그가 리스트 형식인지 검증"""
        if not isinstance(value, list):
            raise serializers.ValidationError("태그는 배열 형식이어야 합니다.")
        return value

    def validate_order(self, value):
        """정렬 순서는 0 이상이어야 함"""
        if value < 0:
            raise serializers.ValidationError("순서는 0 이상이어야 합니다.")
        return value

    def to_representation(self, instance):
        """원본 S3 URL 반환 (웹사이트 콘텐츠는 영구 접근 가능)"""
        data = super().to_representation(instance)

        # 웹사이트 콘텐츠 이미지는 직접 S3 URL 사용
        # Presigned URL이 아닌 영구 접근 가능한 URL이 필요

        return data


# ============================================================================
# 프로젝트 소개 Serializers (Project Feature Serializers)
# ============================================================================

class ProjectFeatureSerializer(serializers.ModelSerializer):
    """프로젝트 특징 시리얼라이저"""

    class Meta:
        model = ProjectFeature
        fields = [
            'id', 'icon', 'title_ko', 'title_en',
            'description_ko', 'description_en', 'order', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_order(self, value):
        """정렬 순서는 0 이상이어야 함"""
        if value < 0:
            raise serializers.ValidationError("순서는 0 이상이어야 합니다.")
        return value


# ============================================================================
# 전략 로드맵 Serializers (Strategy Roadmap Serializers)
# ============================================================================

class StrategyPhaseSerializer(serializers.ModelSerializer):
    """전략 로드맵 페이즈 시리얼라이저"""

    class Meta:
        model = StrategyPhase
        fields = [
            'id', 'icon', 'title_ko', 'title_en',
            'description_ko', 'description_en', 'features_ko', 'features_en', 'order', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_features_ko(self, value):
        """features_ko가 리스트 형식인지 검증"""
        if not isinstance(value, list):
            raise serializers.ValidationError("features_ko는 배열 형식이어야 합니다.")
        return value

    def validate_features_en(self, value):
        """features_en이 리스트 형식인지 검증"""
        if not isinstance(value, list):
            raise serializers.ValidationError("features_en는 배열 형식이어야 합니다.")
        return value

    def validate_order(self, value):
        """정렬 순서는 0 이상이어야 함"""
        if value < 0:
            raise serializers.ValidationError("순서는 0 이상이어야 합니다.")
        return value


# ============================================================================
# 개발 일정 관리 Serializers (Development Timeline Serializers)
# ============================================================================

class DevelopmentTimelineSerializer(serializers.ModelSerializer):
    """개발 일정 시리얼라이저"""

    class Meta:
        model = DevelopmentTimeline
        fields = [
            'id', 'quarter', 'status_icon', 'title_ko', 'title_en',
            'description_ko', 'description_en', 'order', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_order(self, value):
        """정렬 순서는 0 이상이어야 함"""
        if value < 0:
            raise serializers.ValidationError("순서는 0 이상이어야 합니다.")
        return value


# ============================================================================
# 토큰 에코시스템 Serializers (Token Ecosystem Serializers)
# ============================================================================

class TokenEcosystemSerializer(serializers.ModelSerializer):
    """토큰 에코시스템 시리얼라이저"""

    class Meta:
        model = TokenEcosystem
        fields = [
            'id', 'icon', 'name', 'symbol',
            'description_ko', 'description_en', 'features_ko', 'features_en',
            'total_supply', 'current_price', 'order', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_features_ko(self, value):
        """features_ko가 리스트 형식인지 검증"""
        if not isinstance(value, list):
            raise serializers.ValidationError("features_ko는 배열 형식이어야 합니다.")
        return value

    def validate_features_en(self, value):
        """features_en이 리스트 형식인지 검증"""
        if not isinstance(value, list):
            raise serializers.ValidationError("features_en는 배열 형식이어야 합니다.")
        return value

    def validate_order(self, value):
        """정렬 순서는 0 이상이어야 함"""
        if value < 0:
            raise serializers.ValidationError("순서는 0 이상이어야 합니다.")
        return value


# ============================================================================
# 뉴스/보도자료 Serializers (News Article Serializers)
# ============================================================================

class NewsArticleSerializer(serializers.ModelSerializer):
    """뉴스 및 보도자료 시리얼라이저"""

    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title_ko', 'title_en', 'content_ko', 'content_en',
            'image_url', 'external_url', 'publication_date', 'status',
            'order', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_order(self, value):
        """정렬 순서는 0 이상이어야 함"""
        if value < 0:
            raise serializers.ValidationError("순서는 0 이상이어야 합니다.")
        return value

    def validate_status(self, value):
        """상태 값 검증"""
        allowed_statuses = ['draft', 'published', 'archived']
        if value not in allowed_statuses:
            raise serializers.ValidationError(
                f"상태는 {', '.join(allowed_statuses)} 중 하나여야 합니다."
            )
        return value


# ============================================================================
# 이메일 인증 Serializers (Email Verification Serializers)
# ============================================================================

class EmailRegistrationSerializer(serializers.Serializer):
    """이메일 회원가입 요청 시리얼라이저"""
    email = serializers.EmailField()

    def validate_email(self, value):
        """이메일 중복 검증"""
        if SolanaUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 등록된 이메일 주소입니다.")
        return value


class VerificationCodeSerializer(serializers.Serializer):
    """인증 코드 검증 시리얼라이저"""
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)

    def validate_code(self, value):
        """6자리 숫자인지 검증"""
        if not value.isdigit():
            raise serializers.ValidationError("인증 코드는 6자리 숫자여야 합니다.")
        return value


class CompleteRegistrationSerializer(serializers.Serializer):
    """회원가입 완료 시리얼라이저"""
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

    def validate_username(self, value):
        """사용자 이름 중복 검증"""
        if SolanaUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용 중인 사용자 이름입니다.")
        return value

    def validate_password(self, value):
        """비밀번호 강도 검증"""
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError("비밀번호는 대문자를 포함해야 합니다.")
        if not any(c.islower() for c in value):
            raise serializers.ValidationError("비밀번호는 소문자를 포함해야 합니다.")
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError("비밀번호는 숫자를 포함해야 합니다.")
        return value
