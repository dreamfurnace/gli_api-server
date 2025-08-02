from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BusinessContentViewSet, ShoppingCategoryViewSet, ShoppingProductViewSet,
    RWACategoryViewSet, RWAAssetViewSet, InvestmentViewSet,
    ShoppingOrderViewSet, DashboardStatsViewSet, UserProfileViewSet
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
router.register(r'user', UserProfileViewSet, basename='userprofile')

app_name = 'gli_content'

urlpatterns = [
    path('api/v1/', include(router.urls)),
    # Add direct profile endpoint to match frontend expectations
    path('api/user/profile/', UserProfileViewSet.as_view({'get': 'get_profile', 'patch': 'update_profile'}), name='user_profile'),
]