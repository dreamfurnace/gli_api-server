from rest_framework import serializers
from .models import (
    BusinessContent, ShoppingCategory, ShoppingProduct,
    RWACategory, RWAAsset, RWAAssetImage, Investment,
    ShoppingOrder, ShoppingOrderItem
)


class BusinessContentSerializer(serializers.ModelSerializer):
    section_display = serializers.CharField(source='get_section_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = BusinessContent
        fields = [
            'id', 'section', 'section_display', 'title', 'subtitle', 
            'content', 'image_url', 'order', 'status', 'status_display',
            'meta_data', 'created_at', 'updated_at'
        ]


class ShoppingCategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCategory
        fields = [
            'id', 'name', 'name_en', 'description', 'description_en', 'icon', 'order',
            'is_active', 'product_count', 'created_at', 'updated_at'
        ]

    def get_product_count(self, obj):
        return obj.products.filter(status='active').count()


class ShoppingProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    product_type_display = serializers.CharField(source='get_product_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = ShoppingProduct
        fields = [
            'id', 'category', 'category_name', 'name', 'name_en', 'description', 'description_en',
            'short_description', 'short_description_en', 'product_type', 'product_type_display',
            'price_glil', 'price_usd', 'stock_quantity', 'unlimited_stock',
            'main_image_url', 'image_urls', 'status', 'status_display',
            'is_featured', 'tags', 'attributes', 'view_count',
            'purchase_count', 'is_in_stock', 'created_at', 'updated_at'
        ]


class ShoppingProductListSerializer(serializers.ModelSerializer):
    """상품 목록용 간소화된 시리얼라이저"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    product_type_display = serializers.CharField(source='get_product_type_display', read_only=True)
    is_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = ShoppingProduct
        fields = [
            'id', 'category_name', 'name', 'name_en', 'short_description', 'short_description_en',
            'product_type_display', 'price_glil', 'price_usd',
            'main_image_url', 'status', 'is_featured', 'is_in_stock'
        ]


class RWACategorySerializer(serializers.ModelSerializer):
    asset_count = serializers.SerializerMethodField()

    class Meta:
        model = RWACategory
        fields = [
            'id', 'name', 'description', 'icon', 'order',
            'is_active', 'asset_count', 'created_at', 'updated_at'
        ]

    def get_asset_count(self, obj):
        return obj.assets.filter(status='active').count()


class RWAAssetImageSerializer(serializers.ModelSerializer):
    """RWA 자산 이미지 시리얼라이저"""
    class Meta:
        model = RWAAssetImage
        fields = [
            'id', 'asset', 'image_url', 'order', 'is_primary',
            'alt_text', 'alt_text_en', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RWAAssetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    risk_level_display = serializers.CharField(source='get_risk_level_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    operation_type_display = serializers.CharField(source='get_operation_type_display', read_only=True)
    funding_progress = serializers.ReadOnlyField()
    isActive = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = RWAAsset
        fields = [
            'id', 'category', 'category_name',
            'name', 'name_en', 'description', 'description_en',
            'short_description', 'short_description_en',
            'total_value_usd', 'min_investment_glib',
            'max_investment_glib', 'expected_apy', 'historical_returns',
            'risk_level', 'risk_level_display', 'risk_factors',
            'investment_period_months', 'lock_period_months',
            'asset_location', 'asset_location_en', 'asset_type', 'asset_type_en',
            'area_sqm', 'operation_type', 'operation_type_display',
            'underlying_assets',
            'main_image_url', 'image_urls', 'images', 'document_urls',
            'total_invested_glib', 'investor_count', 'funding_target_glib',
            'funding_progress', 'status', 'status_display', 'is_featured', 'order',
            'isActive', 'metadata', 'created_at', 'updated_at'
        ]

    def get_isActive(self, obj):
        return obj.status == 'active'

    def get_images(self, obj):
        """이미지 목록 반환 - RWAAssetImage와 main_image_url 모두 포함 (RWAAssetImage 우선)"""
        images = []

        # RWAAssetImage 테이블의 이미지들 (order 순으로)
        if obj.images.exists():
            images.extend(RWAAssetImageSerializer(obj.images.order_by('order'), many=True).data)

        # main_image_url도 포함 (레거시 데이터, RWAAssetImage에 없는 경우만)
        if obj.main_image_url:
            existing_urls = [img['image_url'] for img in images]
            if obj.main_image_url not in existing_urls:
                # RWAAssetImage 중 is_primary인 이미지가 있는지 확인
                has_primary = any(img.get('is_primary') for img in images)

                # 레거시 이미지 생성
                legacy_image = {
                    'id': None,
                    'image_url': obj.main_image_url,
                    'order': 9999,  # 임시 큰 값
                    'is_primary': not has_primary,  # primary 이미지가 없을 때만 True
                    'alt_text': obj.name,
                    'alt_text_en': obj.name_en or obj.name,
                    'created_at': obj.created_at.isoformat() if obj.created_at else None,
                    'updated_at': obj.updated_at.isoformat() if obj.updated_at else None
                }

                # RWAAssetImage가 없으면 0번에, 있으면 맨 뒤에
                if not images:
                    legacy_image['order'] = 0
                    images.append(legacy_image)
                else:
                    legacy_image['order'] = len(images)
                    images.append(legacy_image)

        # order 순으로 정렬하고 0부터 순차적으로 재정렬
        images.sort(key=lambda x: x['order'])
        for idx, img in enumerate(images):
            img['order'] = idx

        return images


class RWAAssetListSerializer(serializers.ModelSerializer):
    """RWA 자산 목록용 간소화된 시리얼라이저"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    risk_level_display = serializers.CharField(source='get_risk_level_display', read_only=True)
    funding_progress = serializers.ReadOnlyField()
    isActive = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = RWAAsset
        fields = [
            'id', 'category_name',
            'name', 'name_en',
            'short_description', 'short_description_en',
            'description', 'description_en',
            'expected_apy', 'risk_level_display', 'risk_level',
            'min_investment_glib', 'max_investment_glib', 'investment_period_months',
            'total_value_usd', 'total_invested_glib',
            'main_image_url', 'images', 'funding_progress', 'status', 'is_featured', 'order',
            'isActive', 'asset_type', 'asset_location', 'asset_location_en',
            'created_at', 'updated_at'
        ]

    def get_isActive(self, obj):
        return obj.status == 'active'

    def get_images(self, obj):
        """이미지 목록 반환 - RWAAssetImage와 main_image_url 모두 포함 (RWAAssetImage 우선)"""
        images = []

        # RWAAssetImage 테이블의 이미지들 (order 순으로)
        if obj.images.exists():
            images.extend(RWAAssetImageSerializer(obj.images.order_by('order'), many=True).data)

        # main_image_url도 포함 (레거시 데이터, RWAAssetImage에 없는 경우만)
        if obj.main_image_url:
            existing_urls = [img['image_url'] for img in images]
            if obj.main_image_url not in existing_urls:
                # RWAAssetImage 중 is_primary인 이미지가 있는지 확인
                has_primary = any(img.get('is_primary') for img in images)

                # 레거시 이미지 생성
                legacy_image = {
                    'id': None,
                    'image_url': obj.main_image_url,
                    'order': 9999,  # 임시 큰 값
                    'is_primary': not has_primary,  # primary 이미지가 없을 때만 True
                    'alt_text': obj.name,
                    'alt_text_en': obj.name_en or obj.name,
                    'created_at': obj.created_at.isoformat() if obj.created_at else None,
                    'updated_at': obj.updated_at.isoformat() if obj.updated_at else None
                }

                # RWAAssetImage가 없으면 0번에, 있으면 맨 뒤에
                if not images:
                    legacy_image['order'] = 0
                    images.append(legacy_image)
                else:
                    legacy_image['order'] = len(images)
                    images.append(legacy_image)

        # order 순으로 정렬하고 0부터 순차적으로 재정렬
        images.sort(key=lambda x: x['order'])
        for idx, img in enumerate(images):
            img['order'] = idx

        return images


class InvestmentSerializer(serializers.ModelSerializer):
    investor_name = serializers.CharField(source='investor.username', read_only=True)
    rwa_asset_name = serializers.CharField(source='rwa_asset.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    current_profit_loss = serializers.ReadOnlyField()
    profit_loss_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Investment
        fields = [
            'id', 'investor', 'investor_name', 'rwa_asset', 'rwa_asset_name',
            'amount_glib', 'amount_usd_at_time', 'investment_date',
            'expected_return_date', 'lock_end_date', 'expected_apy_at_time',
            'current_value_glib', 'realized_profit_glib', 'current_profit_loss',
            'profit_loss_percentage', 'status', 'status_display',
            'investment_tx_hash', 'withdrawal_tx_hash', 'metadata'
        ]


class InvestmentCreateSerializer(serializers.ModelSerializer):
    """투자 생성용 시리얼라이저"""
    class Meta:
        model = Investment
        fields = [
            'rwa_asset', 'amount_glib', 'amount_usd_at_time',
            'expected_return_date', 'lock_end_date', 'expected_apy_at_time'
        ]
    
    def create(self, validated_data):
        # 현재 사용자를 investor로 설정
        validated_data['investor'] = self.context['request'].user
        return super().create(validated_data)


class ShoppingOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(read_only=True)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = ShoppingOrderItem
        fields = [
            'id', 'product', 'product_name', 'product_price_glil',
            'quantity', 'selected_attributes', 'total_price'
        ]


class ShoppingOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items = ShoppingOrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = ShoppingOrder
        fields = [
            'id', 'customer', 'customer_name', 'order_number',
            'total_amount_glil', 'total_amount_usd', 'status', 'status_display',
            'payment_tx_hash', 'paid_at', 'shipping_address',
            'tracking_number', 'shipped_at', 'delivered_at',
            'notes', 'metadata', 'items', 'created_at', 'updated_at'
        ]


class ShoppingOrderCreateSerializer(serializers.ModelSerializer):
    """주문 생성용 시리얼라이저"""
    items = ShoppingOrderItemSerializer(many=True)
    
    class Meta:
        model = ShoppingOrder
        fields = [
            'total_amount_glil', 'total_amount_usd', 'shipping_address',
            'notes', 'items'
        ]
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # 주문 번호 생성
        import uuid
        from django.utils import timezone
        order_number = f"GLI{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        
        # 현재 사용자를 customer로 설정
        validated_data['customer'] = self.context['request'].user
        validated_data['order_number'] = order_number
        
        order = ShoppingOrder.objects.create(**validated_data)
        
        # 주문 항목 생성
        for item_data in items_data:
            product = item_data['product']
            item_data['product_name'] = product.name
            item_data['product_price_glil'] = product.price_glil
            ShoppingOrderItem.objects.create(order=order, **item_data)
        
        return order


# 통계 및 대시보드용 시리얼라이저
class InvestmentStatsSerializer(serializers.Serializer):
    """투자 통계용 시리얼라이저"""
    total_invested = serializers.DecimalField(max_digits=20, decimal_places=8)
    total_current_value = serializers.DecimalField(max_digits=20, decimal_places=8)
    total_profit_loss = serializers.DecimalField(max_digits=20, decimal_places=8)
    profit_loss_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    active_investments_count = serializers.IntegerField()
    completed_investments_count = serializers.IntegerField()


class RWAAssetStatsSerializer(serializers.Serializer):
    """RWA 자산 통계용 시리얼라이저"""
    total_assets = serializers.IntegerField()
    active_assets = serializers.IntegerField()
    total_value_usd = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_invested_glib = serializers.DecimalField(max_digits=20, decimal_places=8)
    average_apy = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_investors = serializers.IntegerField()