from rest_framework import serializers
from .models import SolanaUser, AuthNonce, SolanaTransaction


class SolanaUserSerializer(serializers.ModelSerializer):
    """솔라나 사용자 시리얼라이저"""
    
    class Meta:
        model = SolanaUser
        fields = [
            'id', 'wallet_address', 'email', 'username', 
            'first_name', 'last_name', 'membership_level',
            'sol_balance', 'last_balance_update', 'is_active',
            'created_at', 'updated_at', 'last_login'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_login']


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