from django.contrib import admin
from .models import SolanaUser, AuthNonce, SolanaTransaction


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
    list_display = ['wallet_address', 'nonce', 'used', 'created_at']
    list_filter = ['used', 'created_at']
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