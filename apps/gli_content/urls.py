from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BusinessContentViewSet, ShoppingCategoryViewSet, ShoppingProductViewSet,
    RWACategoryViewSet, RWAAssetViewSet, InvestmentViewSet,
    ShoppingOrderViewSet, DashboardStatsViewSet
)

# DRF Router 설정
router = DefaultRouter()
router.register(r'business-content', BusinessContentViewSet, basename='businesscontent')
router.register(r'shopping/categories', ShoppingCategoryViewSet, basename='shoppingcategory')
router.register(r'shopping/products', ShoppingProductViewSet, basename='shoppingproduct')
router.register(r'rwa/categories', RWACategoryViewSet, basename='rwacategory')
router.register(r'rwa/assets', RWAAssetViewSet, basename='rwaasset')
router.register(r'investments', InvestmentViewSet, basename='investment')
router.register(r'shopping/orders', ShoppingOrderViewSet, basename='shoppingorder')
router.register(r'dashboard', DashboardStatsViewSet, basename='dashboard')

app_name = 'gli_content'

urlpatterns = [
    path('api/v1/', include(router.urls)),
]