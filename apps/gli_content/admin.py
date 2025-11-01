from django.contrib import admin
from django.utils.html import format_html
from .models import (
    BusinessContent, ShoppingCategory, ShoppingProduct,
    RWACategory, RWAAsset, RWAAssetImage, Investment,
    ShoppingOrder, ShoppingOrderItem
)


@admin.register(BusinessContent)
class BusinessContentAdmin(admin.ModelAdmin):
    list_display = ('section', 'title', 'status', 'order', 'created_at')
    list_filter = ('section', 'status', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('section', 'order')
    list_editable = ('order', 'status')
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('section', 'title', 'subtitle', 'content')
        }),
        ('표시 설정', {
            'fields': ('order', 'status', 'image_url')
        }),
        ('메타데이터', {
            'fields': ('meta_data',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ShoppingCategory)
class ShoppingCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'product_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('order', 'name')
    list_editable = ('order', 'is_active')
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = '상품 수'


@admin.register(ShoppingProduct)
class ShoppingProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'product_type', 'price_glil', 'status', 'is_featured', 'stock_info')
    list_filter = ('category', 'product_type', 'status', 'is_featured', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-is_featured', '-created_at')
    list_editable = ('status', 'is_featured')
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('category', 'name', 'description', 'short_description', 'product_type')
        }),
        ('가격 및 재고', {
            'fields': ('price_glil', 'price_usd', 'stock_quantity', 'unlimited_stock')
        }),
        ('이미지 및 미디어', {
            'fields': ('main_image_url', 'image_urls')
        }),
        ('상태 및 옵션', {
            'fields': ('status', 'is_featured', 'tags', 'attributes')
        }),
        ('통계', {
            'fields': ('view_count', 'purchase_count'),
            'classes': ('collapse',)
        }),
    )
    
    def stock_info(self, obj):
        if obj.unlimited_stock:
            return format_html('<span style="color: green;">무제한</span>')
        elif obj.stock_quantity > 0:
            return f'{obj.stock_quantity}개'
        else:
            return format_html('<span style="color: red;">품절</span>')
    stock_info.short_description = '재고'


@admin.register(RWACategory)
class RWACategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'asset_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('order', 'name')
    list_editable = ('order', 'is_active')
    
    def asset_count(self, obj):
        return obj.assets.count()
    asset_count.short_description = '투자 자산 수'


class RWAAssetImageInline(admin.TabularInline):
    model = RWAAssetImage
    extra = 1
    max_num = 5
    fields = ('image_url', 'order', 'is_primary', 'alt_text', 'alt_text_en')
    ordering = ('order', '-is_primary')


@admin.register(RWAAsset)
class RWAAssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'expected_apy', 'risk_level', 'status', 'funding_progress_display', 'is_featured', 'image_count')
    list_filter = ('category', 'risk_level', 'status', 'is_featured', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-is_featured', '-created_at')
    list_editable = ('status', 'is_featured')
    inlines = [RWAAssetImageInline]
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('category', 'name', 'description', 'short_description')
        }),
        ('투자 조건', {
            'fields': ('total_value_usd', 'min_investment_glib', 'max_investment_glib', 'funding_target_glib')
        }),
        ('수익률 및 위험', {
            'fields': ('expected_apy', 'historical_returns', 'risk_level', 'risk_factors')
        }),
        ('투자 기간', {
            'fields': ('investment_period_months', 'lock_period_months')
        }),
        ('자산 정보', {
            'fields': ('asset_location', 'asset_type', 'underlying_assets')
        }),
        ('이미지 및 문서', {
            'fields': ('main_image_url', 'image_urls', 'document_urls')
        }),
        ('상태 및 옵션', {
            'fields': ('status', 'is_featured')
        }),
        ('현재 투자 현황', {
            'fields': ('total_invested_glib', 'investor_count'),
            'classes': ('collapse',)
        }),
        ('메타데이터', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )
    
    def funding_progress_display(self, obj):
        progress = obj.funding_progress
        color = 'green' if progress >= 80 else 'orange' if progress >= 50 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, progress
        )
    funding_progress_display.short_description = '펀딩 진행률'

    def image_count(self, obj):
        count = obj.images.count()
        has_primary = obj.images.filter(is_primary=True).exists()
        if has_primary:
            return format_html(
                '<span style="color: green;">{}/5 ✓</span>',
                count
            )
        elif count > 0:
            return format_html(
                '<span style="color: orange;">{}/5</span>',
                count
            )
        return format_html('<span style="color: red;">0/5</span>')
    image_count.short_description = '이미지'


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('investor', 'rwa_asset', 'amount_glib', 'status', 'profit_loss_display', 'investment_date')
    list_filter = ('status', 'rwa_asset__category', 'investment_date')
    search_fields = ('investor__username', 'rwa_asset__name')
    ordering = ('-investment_date',)
    readonly_fields = ('current_profit_loss', 'profit_loss_percentage')
    
    fieldsets = (
        ('투자 정보', {
            'fields': ('investor', 'rwa_asset', 'amount_glib', 'amount_usd_at_time')
        }),
        ('투자 조건', {
            'fields': ('investment_date', 'expected_return_date', 'lock_end_date', 'expected_apy_at_time')
        }),
        ('수익 현황', {
            'fields': ('current_value_glib', 'realized_profit_glib', 'current_profit_loss', 'profit_loss_percentage')
        }),
        ('상태 및 트랜잭션', {
            'fields': ('status', 'investment_tx_hash', 'withdrawal_tx_hash')
        }),
        ('메타데이터', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )
    
    def profit_loss_display(self, obj):
        profit_loss = obj.current_profit_loss
        percentage = obj.profit_loss_percentage
        color = 'green' if profit_loss > 0 else 'red' if profit_loss < 0 else 'black'
        return format_html(
            '<span style="color: {};">{:.8f} GLIB ({:+.2f}%)</span>',
            color, profit_loss, percentage
        )
    profit_loss_display.short_description = '손익'


class ShoppingOrderItemInline(admin.TabularInline):
    model = ShoppingOrderItem
    extra = 0
    readonly_fields = ('total_price',)


@admin.register(ShoppingOrder)
class ShoppingOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'total_amount_glil', 'status', 'created_at', 'paid_at')
    list_filter = ('status', 'created_at', 'paid_at')
    search_fields = ('order_number', 'customer__username')
    ordering = ('-created_at',)
    inlines = [ShoppingOrderItemInline]
    
    fieldsets = (
        ('주문 정보', {
            'fields': ('customer', 'order_number', 'total_amount_glil', 'total_amount_usd')
        }),
        ('결제 정보', {
            'fields': ('status', 'payment_tx_hash', 'paid_at')
        }),
        ('배송 정보', {
            'fields': ('shipping_address', 'tracking_number', 'shipped_at', 'delivered_at')
        }),
        ('기타', {
            'fields': ('notes', 'metadata'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ShoppingOrderItem)
class ShoppingOrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'product_price_glil', 'total_price')
    list_filter = ('order__status', 'order__created_at')
    search_fields = ('product_name', 'order__order_number')
    ordering = ('-order__created_at',)