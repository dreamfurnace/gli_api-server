from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.solana_auth.models import SolanaUser
import uuid


class BaseTimestampModel(models.Model):
    """기본 타임스탬프 모델"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class BusinessContent(BaseTimestampModel):
    """사업소개 콘텐츠 모델"""
    SECTION_CHOICES = [
        ('background', '회사 소개'),
        ('team', '사업 소개'),
        ('strategy', '사업 계획'),
        ('roadmap', '생태계 토큰'),
        ('tokens', '추진 사업'),
    ]
    
    STATUS_CHOICES = [
        ('draft', '초안'),
        ('published', '게시됨'),
        ('archived', '보관됨'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, db_index=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    meta_data = models.JSONField(default=dict, blank=True)  # 추가 메타데이터
    
    class Meta:
        db_table = 'business_contents'
        ordering = ['section', 'order']
        unique_together = ['section', 'order']
    
    def __str__(self):
        return f"{self.get_section_display()}: {self.title}"


class ShoppingCategory(BaseTimestampModel):
    """쇼핑몰 카테고리 모델"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)  # 이모지 또는 아이콘 클래스
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'shopping_categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class ShoppingProduct(BaseTimestampModel):
    """쇼핑몰 상품 모델"""
    PRODUCT_TYPE_CHOICES = [
        ('goods', '일반 상품'),
        ('resort', '리조트 예약'),
        ('restaurant', '레스토랑 예약'),
        ('service', '서비스'),
    ]
    
    STATUS_CHOICES = [
        ('active', '활성'),
        ('inactive', '비활성'),
        ('sold_out', '품절'),
        ('discontinued', '단종'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(ShoppingCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default='goods')
    
    # 가격 정보 (GLI-L 토큰으로 결제)
    price_glil = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # 재고 관리
    stock_quantity = models.PositiveIntegerField(default=0)
    unlimited_stock = models.BooleanField(default=False)
    
    # 이미지 및 미디어
    main_image_url = models.URLField(blank=True)
    image_urls = models.JSONField(default=list, blank=True)  # 추가 이미지들
    
    # 상태 및 메타데이터
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True)  # 태그 리스트
    attributes = models.JSONField(default=dict, blank=True)  # 상품 속성 (크기, 색상 등)
    
    # 통계
    view_count = models.PositiveIntegerField(default=0)
    purchase_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'shopping_products'
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['category', 'status']),
            models.Index(fields=['product_type', 'status']),
            models.Index(fields=['-is_featured', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.price_glil} GLIL)"
    
    @property
    def is_in_stock(self):
        return self.unlimited_stock or self.stock_quantity > 0


class RWACategory(BaseTimestampModel):
    """RWA 투자 자산 카테고리"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'rwa_categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class RWAAsset(BaseTimestampModel):
    """RWA 투자 자산 모델"""
    RISK_LEVEL_CHOICES = [
        ('low', '낮음'),
        ('medium', '보통'),
        ('high', '높음'),
        ('very_high', '매우 높음'),
    ]
    
    STATUS_CHOICES = [
        ('draft', '초안'),
        ('active', '투자 가능'),
        ('paused', '일시 중단'),
        ('completed', '완료'),
        ('cancelled', '취소'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(RWACategory, on_delete=models.CASCADE, related_name='assets')
    
    # 기본 정보
    name = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    
    # 투자 정보
    total_value_usd = models.DecimalField(max_digits=15, decimal_places=2)
    min_investment_gleb = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
    max_investment_gleb = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    
    # 수익률 정보
    expected_apy = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    historical_returns = models.JSONField(default=list, blank=True)  # 과거 수익률 데이터
    
    # 위험도 및 등급
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default='medium')
    risk_factors = models.JSONField(default=list, blank=True)  # 위험 요소들
    
    # 투자 기간
    investment_period_months = models.PositiveIntegerField()
    lock_period_months = models.PositiveIntegerField(default=0)  # 락업 기간
    
    # 자산 세부 정보
    asset_location = models.CharField(max_length=200, blank=True)
    asset_type = models.CharField(max_length=100)  # 부동산, 주식, 채권 등
    underlying_assets = models.JSONField(default=dict, blank=True)  # 기초 자산 정보
    
    # 이미지 및 문서
    main_image_url = models.URLField(blank=True)
    image_urls = models.JSONField(default=list, blank=True)
    document_urls = models.JSONField(default=list, blank=True)  # 투자 설명서 등
    
    # 투자 현황
    total_invested_gleb = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    investor_count = models.PositiveIntegerField(default=0)
    funding_target_gleb = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    
    # 상태 및 기타
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    
    # 메타데이터
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'rwa_assets'
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['category', 'status']),
            models.Index(fields=['risk_level', 'status']),
            models.Index(fields=['-is_featured', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.expected_apy}% APY)"
    
    @property
    def funding_progress(self):
        if not self.funding_target_gleb:
            return 0
        return min((self.total_invested_gleb / self.funding_target_gleb) * 100, 100)


class Investment(BaseTimestampModel):
    """투자 내역 모델"""
    STATUS_CHOICES = [
        ('pending', '처리 중'),
        ('confirmed', '확정'),
        ('active', '투자 중'),
        ('completed', '완료'),
        ('cancelled', '취소'),
        ('failed', '실패'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    investor = models.ForeignKey(SolanaUser, on_delete=models.CASCADE, related_name='investments')
    rwa_asset = models.ForeignKey(RWAAsset, on_delete=models.CASCADE, related_name='investments')
    
    # 투자 금액
    amount_gleb = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
    amount_usd_at_time = models.DecimalField(max_digits=15, decimal_places=2)  # 투자 시점의 USD 가치
    
    # 투자 조건
    investment_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField()
    lock_end_date = models.DateTimeField(null=True, blank=True)
    
    # 수익률 및 수익
    expected_apy_at_time = models.DecimalField(max_digits=5, decimal_places=2)
    current_value_gleb = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    realized_profit_gleb = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    
    # 투자 상태
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # 트랜잭션 정보
    investment_tx_hash = models.CharField(max_length=100, blank=True)  # 투자 트랜잭션 해시
    withdrawal_tx_hash = models.CharField(max_length=100, blank=True)  # 출금 트랜잭션 해시
    
    # 메타데이터
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'investments'
        ordering = ['-investment_date']
        indexes = [
            models.Index(fields=['investor', 'status']),
            models.Index(fields=['rwa_asset', 'status']),
            models.Index(fields=['-investment_date']),
        ]
    
    def __str__(self):
        return f"{self.investor.username} -> {self.rwa_asset.name} ({self.amount_gleb} GLEB)"
    
    @property
    def current_profit_loss(self):
        return self.current_value_gleb - self.amount_gleb
    
    @property
    def profit_loss_percentage(self):
        if self.amount_gleb == 0:
            return 0
        return ((self.current_value_gleb - self.amount_gleb) / self.amount_gleb) * 100


class ShoppingOrder(BaseTimestampModel):
    """쇼핑몰 주문 모델"""
    STATUS_CHOICES = [
        ('pending', '결제 대기'),
        ('paid', '결제 완료'),
        ('processing', '처리 중'),
        ('shipped', '발송됨'),
        ('delivered', '배송 완료'),
        ('cancelled', '취소'),
        ('refunded', '환불 완료'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(SolanaUser, on_delete=models.CASCADE, related_name='orders')
    
    # 주문 정보
    order_number = models.CharField(max_length=50, unique=True, db_index=True)
    total_amount_glil = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
    total_amount_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # 상태 및 결제
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_tx_hash = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # 배송 정보
    shipping_address = models.JSONField(default=dict, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # 메타데이터
    notes = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'shopping_orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['order_number']),
        ]
    
    def __str__(self):
        return f"Order {self.order_number} - {self.customer.username}"


class ShoppingOrderItem(BaseTimestampModel):
    """주문 상품 항목"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(ShoppingOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ShoppingProduct, on_delete=models.CASCADE)
    
    # 주문 시점의 정보 (가격 변동 대비)
    product_name = models.CharField(max_length=200)
    product_price_glil = models.DecimalField(max_digits=20, decimal_places=8)
    quantity = models.PositiveIntegerField(default=1)
    
    # 선택된 옵션 (크기, 색상 등)
    selected_attributes = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'shopping_order_items'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
    
    @property
    def total_price(self):
        return self.product_price_glil * self.quantity