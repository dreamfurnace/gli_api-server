from django.contrib.auth.models import AbstractUser
from django.db import models
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