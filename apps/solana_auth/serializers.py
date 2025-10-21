from rest_framework import serializers
from .models import SolanaUser, AuthNonce, SolanaTransaction, FaceVerification, AdminGrade, AdminUser, AdminPermission, GradePermission, TeamMember, ProjectFeature, StrategyPhase, DevelopmentTimeline, TokenEcosystem


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
    livenessScore = serializers.DecimalField(max_digits=5, decimal_places=4)
    timestamp = serializers.DateTimeField()
    attempts = serializers.IntegerField(default=1)
    checkDetails = CheckDetailSerializer(many=True, required=False, allow_null=True)

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
