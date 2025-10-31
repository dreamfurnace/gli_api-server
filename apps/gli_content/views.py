from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from decimal import Decimal

from .models import (
    BusinessContent, ShoppingCategory, ShoppingProduct,
    RWACategory, RWAAsset, RWAAssetImage, Investment,
    ShoppingOrder, ShoppingOrderItem
)
from .serializers import (
    BusinessContentSerializer, ShoppingCategorySerializer,
    ShoppingProductSerializer, ShoppingProductListSerializer,
    RWACategorySerializer, RWAAssetSerializer, RWAAssetListSerializer,
    RWAAssetImageSerializer,
    InvestmentSerializer, InvestmentCreateSerializer,
    ShoppingOrderSerializer, ShoppingOrderCreateSerializer,
    InvestmentStatsSerializer, RWAAssetStatsSerializer
)


class BusinessContentViewSet(viewsets.ModelViewSet):
    """사업소개 콘텐츠 API"""
    queryset = BusinessContent.objects.filter(status='published')
    serializer_class = BusinessContentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['section', 'status']
    ordering = ['section', 'order']
    
    @action(detail=False, methods=['get'])
    def by_section(self, request):
        """섹션별 콘텐츠 조회"""
        section = request.query_params.get('section')
        if not section:
            return Response(
                {'error': 'section parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        contents = self.queryset.filter(section=section)
        serializer = self.get_serializer(contents, many=True)
        return Response(serializer.data)


class ShoppingCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """쇼핑몰 카테고리 API"""
    queryset = ShoppingCategory.objects.filter(is_active=True)
    serializer_class = ShoppingCategorySerializer
    ordering = ['order', 'name']


class ShoppingProductViewSet(viewsets.ReadOnlyModelViewSet):
    """쇼핑몰 상품 API"""
    queryset = ShoppingProduct.objects.filter(status='active')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'product_type', 'is_featured']
    search_fields = ['name', 'description', 'tags']
    ordering = ['-is_featured', '-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingProductListSerializer
        return ShoppingProductSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """상품 상세 조회 시 조회수 증가"""
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """추천 상품 목록"""
        featured_products = self.queryset.filter(is_featured=True)[:10]
        serializer = ShoppingProductListSerializer(featured_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """카테고리별 상품 목록"""
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response(
                {'error': 'category_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        products = self.queryset.filter(category_id=category_id)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ShoppingProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ShoppingProductListSerializer(products, many=True)
        return Response(serializer.data)


class RWACategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """RWA 투자 자산 카테고리 API"""
    queryset = RWACategory.objects.filter(is_active=True)
    serializer_class = RWACategorySerializer
    ordering = ['order', 'name']


class RWAAssetViewSet(viewsets.ModelViewSet):
    """RWA 투자 자산 API"""
    queryset = RWAAsset.objects.all()  # 관리자는 모든 상태의 자산을 볼 수 있어야 함
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'risk_level', 'is_featured', 'status']
    search_fields = ['name', 'name_en', 'description', 'description_en', 'asset_type', 'asset_location']
    ordering = ['-is_featured', '-created_at']

    def get_queryset(self):
        """사용자는 active 자산만, 관리자는 모든 자산 조회"""
        queryset = super().get_queryset()
        # 인증되지 않았거나 일반 사용자는 active 자산만
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            queryset = queryset.filter(status='active')
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return RWAAssetListSerializer
        return RWAAssetSerializer

    def get_permissions(self):
        """생성/수정/삭제는 관리자만 가능"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """추천 투자 자산 목록"""
        featured_assets = self.get_queryset().filter(is_featured=True)[:10]
        serializer = RWAAssetListSerializer(featured_assets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def stats(self, request):
        """RWA 자산 통계 (관리자 전용)"""
        queryset = RWAAsset.objects.all()

        # 기본 통계
        total_assets = queryset.count()
        active_assets = queryset.filter(status='active').count()

        # 자산 가치 및 투자 통계
        stats_data = queryset.aggregate(
            total_value=Sum('total_value_usd'),
            total_investment=Sum('total_invested_glib'),
            average_return=Avg('expected_apy'),
        )

        # 위험도별 분포
        risk_distribution = {
            'low': queryset.filter(risk_level='low').count(),
            'medium': queryset.filter(risk_level='medium').count(),
            'high': queryset.filter(risk_level='high').count(),
            'very_high': queryset.filter(risk_level='very_high').count(),
        }

        # 타입별 분포 (asset_type 기준)
        type_stats = queryset.values('asset_type').annotate(
            count=Count('id'),
            total_value=Sum('total_value_usd')
        )

        # 월별 성장 데이터 (최근 6개월)
        from django.utils import timezone
        from datetime import timedelta

        monthly_data = []
        for i in range(6):
            month_start = timezone.now() - timedelta(days=30 * (6 - i))
            month_end = month_start + timedelta(days=30)

            month_assets = queryset.filter(created_at__lte=month_end)
            month_value = month_assets.aggregate(
                value=Sum('total_value_usd'),
                investment=Sum('total_invested_glib')
            )

            monthly_data.append({
                'month': month_start.strftime('%Y-%m'),
                'value': float(month_value['value'] or 0),
                'investment': float(month_value['investment'] or 0)
            })

        return Response({
            'totalAssets': total_assets,
            'activeAssets': active_assets,
            'totalValue': float(stats_data['total_value'] or 0),
            'totalInvestment': float(stats_data['total_investment'] or 0),
            'averageReturn': float(stats_data['average_return'] or 0),
            'riskDistribution': risk_distribution,
            'typeDistribution': list(type_stats),
            'monthlyGrowth': monthly_data
        })
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """카테고리별 투자 자산 목록"""
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response(
                {'error': 'category_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        assets = self.queryset.filter(category_id=category_id)
        page = self.paginate_queryset(assets)
        if page is not None:
            serializer = RWAAssetListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = RWAAssetListSerializer(assets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_risk_level(self, request):
        """위험도별 투자 자산 목록"""
        risk_level = request.query_params.get('risk_level')
        if not risk_level:
            return Response(
                {'error': 'risk_level parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        assets = self.queryset.filter(risk_level=risk_level)
        serializer = RWAAssetListSerializer(assets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser], url_path='status')
    def toggle_status(self, request, pk=None):
        """RWA 자산 상태 토글 (관리자 전용)"""
        rwa_asset = self.get_object()
        is_active = request.data.get('isActive')

        if is_active is None:
            return Response(
                {'error': 'isActive parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # isActive 값에 따라 status 필드 업데이트
        if is_active:
            rwa_asset.status = 'active'
        else:
            rwa_asset.status = 'paused'

        rwa_asset.save(update_fields=['status'])

        serializer = self.get_serializer(rwa_asset)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser], url_path='reorder')
    def reorder_assets(self, request):
        """RWA 자산 순서 변경 (관리자 전용)"""
        asset_ids = request.data.get('assetIds', [])

        if not asset_ids or not isinstance(asset_ids, list):
            return Response(
                {'error': 'assetIds array is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 트랜잭션으로 순서 업데이트
        from django.db import transaction

        try:
            with transaction.atomic():
                for idx, asset_id in enumerate(asset_ids):
                    RWAAsset.objects.filter(id=asset_id).update(order=idx)

            return Response({
                'message': 'Asset order updated successfully',
                'count': len(asset_ids)
            })
        except Exception as e:
            return Response(
                {'error': f'Failed to update order: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def invest(self, request, pk=None):
        """투자하기"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        rwa_asset = self.get_object()
        
        # 투자 가능 상태 확인
        if rwa_asset.status != 'active':
            return Response(
                {'error': 'This asset is not available for investment'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        amount_glib = request.data.get('amount_glib')
        if not amount_glib:
            return Response(
                {'error': 'amount_glib is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        amount_glib = Decimal(str(amount_glib))
        
        # 최소 투자 금액 확인
        if amount_glib < rwa_asset.min_investment_glib:
            return Response(
                {'error': f'Minimum investment amount is {rwa_asset.min_investment_glib} GLIB'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 최대 투자 금액 확인
        if rwa_asset.max_investment_glib and amount_glib > rwa_asset.max_investment_glib:
            return Response(
                {'error': f'Maximum investment amount is {rwa_asset.max_investment_glib} GLIB'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 투자 생성
        investment_data = {
            'rwa_asset': rwa_asset.id,
            'amount_glib': amount_glib,
            'amount_usd_at_time': request.data.get('amount_usd_at_time', 0),
            'expected_apy_at_time': rwa_asset.expected_apy,
            'expected_return_date': timezone.now() + timezone.timedelta(days=rwa_asset.investment_period_months * 30),
            'lock_end_date': timezone.now() + timezone.timedelta(days=rwa_asset.lock_period_months * 30) if rwa_asset.lock_period_months > 0 else None
        }
        
        serializer = InvestmentCreateSerializer(data=investment_data, context={'request': request})
        if serializer.is_valid():
            investment = serializer.save()
            
            # RWA 자산 투자 현황 업데이트
            rwa_asset.total_invested_glib += amount_glib
            rwa_asset.investor_count = rwa_asset.investments.values('investor').distinct().count()
            rwa_asset.save(update_fields=['total_invested_glib', 'investor_count'])
            
            return Response(
                InvestmentSerializer(investment).data, 
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ===== 이미지 관리 액션들 =====

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def upload_image(self, request, pk=None):
        """RWA 자산 이미지 업로드 (최대 5개)"""
        asset = self.get_object()

        # 현재 이미지 개수 확인
        current_image_count = asset.images.count()
        if current_image_count >= 5:
            return Response(
                {'error': '한 자산당 최대 5개의 이미지만 업로드할 수 있습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 이미지 URL 필수
        image_url = request.data.get('image_url')
        if not image_url:
            return Response(
                {'error': 'image_url은 필수입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 순서 자동 설정 (기존 이미지 개수 + 1)
        order = request.data.get('order', current_image_count)
        is_primary = request.data.get('is_primary', current_image_count == 0)  # 첫 이미지는 자동으로 메인

        # 이미지 생성
        image_data = {
            'asset': asset.id,
            'image_url': image_url,
            'order': order,
            'is_primary': is_primary,
            'alt_text': request.data.get('alt_text', ''),
            'alt_text_en': request.data.get('alt_text_en', '')
        }

        serializer = RWAAssetImageSerializer(data=image_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='images/(?P<image_id>[^/.]+)', permission_classes=[permissions.IsAdminUser])
    def delete_image(self, request, pk=None, image_id=None):
        """RWA 자산 이미지 삭제"""
        asset = self.get_object()

        try:
            image = asset.images.get(id=image_id)
            was_primary = image.is_primary
            image.delete()

            # 메인 이미지가 삭제된 경우, 남은 이미지 중 첫 번째를 메인으로 설정
            if was_primary and asset.images.exists():
                first_image = asset.images.order_by('order').first()
                first_image.is_primary = True
                first_image.save()

            return Response(
                {'message': '이미지가 성공적으로 삭제되었습니다.'},
                status=status.HTTP_204_NO_CONTENT
            )
        except RWAAssetImage.DoesNotExist:
            return Response(
                {'error': '이미지를 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['patch'], url_path='images/reorder', permission_classes=[permissions.IsAdminUser])
    def reorder_images(self, request, pk=None):
        """RWA 자산 이미지 순서 재정렬

        Request body:
        {
            "image_orders": [
                {"id": "image_id_1", "order": 0},
                {"id": "image_id_2", "order": 1},
                ...
            ]
        }
        """
        asset = self.get_object()
        image_orders = request.data.get('image_orders', [])

        if not image_orders:
            return Response(
                {'error': 'image_orders는 필수입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 각 이미지의 순서 업데이트
        updated_images = []
        for item in image_orders:
            image_id = item.get('id')
            new_order = item.get('order')

            try:
                image = asset.images.get(id=image_id)
                image.order = new_order
                image.save(update_fields=['order'])
                updated_images.append(image)
            except RWAAssetImage.DoesNotExist:
                pass

        # 업데이트된 이미지 목록 반환
        serializer = RWAAssetImageSerializer(asset.images.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='images/(?P<image_id>[^/.]+)/set-primary', permission_classes=[permissions.IsAdminUser])
    def set_primary_image(self, request, pk=None, image_id=None):
        """특정 이미지를 메인 이미지로 설정"""
        asset = self.get_object()

        try:
            image = asset.images.get(id=image_id)
            image.is_primary = True
            image.save()  # save 메서드에서 자동으로 다른 이미지들의 is_primary를 False로 변경

            return Response(
                RWAAssetImageSerializer(image).data,
                status=status.HTTP_200_OK
            )
        except RWAAssetImage.DoesNotExist:
            return Response(
                {'error': '이미지를 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )


class InvestmentViewSet(viewsets.ReadOnlyModelViewSet):
    """투자 내역 API"""
    serializer_class = InvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'rwa_asset__category']
    ordering = ['-investment_date']
    
    def get_queryset(self):
        # 현재 사용자의 투자 내역만 조회
        return Investment.objects.filter(investor=self.request.user)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """투자 통계"""
        investments = self.get_queryset().filter(status__in=['confirmed', 'active', 'completed'])
        
        stats_data = investments.aggregate(
            total_invested=Sum('amount_glib') or Decimal('0'),
            total_current_value=Sum('current_value_glib') or Decimal('0'),
            active_count=Count('id', filter=Q(status='active')),
            completed_count=Count('id', filter=Q(status='completed'))
        )
        
        total_profit_loss = stats_data['total_current_value'] - stats_data['total_invested']
        profit_loss_percentage = (
            (total_profit_loss / stats_data['total_invested'] * 100) 
            if stats_data['total_invested'] > 0 else Decimal('0')
        )
        
        stats_data.update({
            'total_profit_loss': total_profit_loss,
            'profit_loss_percentage': profit_loss_percentage,
            'active_investments_count': stats_data.pop('active_count'),
            'completed_investments_count': stats_data.pop('completed_count')
        })
        
        serializer = InvestmentStatsSerializer(stats_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def portfolio(self, request):
        """투자 포트폴리오"""
        investments = self.get_queryset().filter(status__in=['active', 'completed'])
        
        # 카테고리별 투자 현황
        category_stats = {}
        for investment in investments:
            category = investment.rwa_asset.category.name
            if category not in category_stats:
                category_stats[category] = {
                    'total_invested': Decimal('0'),
                    'total_current_value': Decimal('0'),
                    'count': 0
                }
            
            category_stats[category]['total_invested'] += investment.amount_glib
            category_stats[category]['total_current_value'] += investment.current_value_glib
            category_stats[category]['count'] += 1
        
        # 위험도별 투자 현황
        risk_stats = {}
        for investment in investments:
            risk_level = investment.rwa_asset.get_risk_level_display()
            if risk_level not in risk_stats:
                risk_stats[risk_level] = {
                    'total_invested': Decimal('0'),
                    'total_current_value': Decimal('0'),
                    'count': 0
                }
            
            risk_stats[risk_level]['total_invested'] += investment.amount_glib
            risk_stats[risk_level]['total_current_value'] += investment.current_value_glib
            risk_stats[risk_level]['count'] += 1
        
        return Response({
            'category_breakdown': category_stats,
            'risk_breakdown': risk_stats,
            'recent_investments': InvestmentSerializer(investments[:5], many=True).data
        })


class ShoppingOrderViewSet(viewsets.ModelViewSet):
    """쇼핑몰 주문 API"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # 현재 사용자의 주문만 조회
        return ShoppingOrder.objects.filter(customer=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ShoppingOrderCreateSerializer
        return ShoppingOrderSerializer
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """주문 취소"""
        order = self.get_object()
        
        if order.status not in ['pending', 'paid']:
            return Response(
                {'error': 'Order cannot be cancelled'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'cancelled'
        order.save(update_fields=['status'])
        
        return Response({'message': 'Order cancelled successfully'})
    
    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        """결제 확인"""
        order = self.get_object()
        
        if order.status != 'pending':
            return Response(
                {'error': 'Order is not in pending status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tx_hash = request.data.get('payment_tx_hash')
        if not tx_hash:
            return Response(
                {'error': 'payment_tx_hash is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'paid'
        order.payment_tx_hash = tx_hash
        order.paid_at = timezone.now()
        order.save(update_fields=['status', 'payment_tx_hash', 'paid_at'])
        
        # 상품 구매 수량 업데이트
        for item in order.items.all():
            if not item.product.unlimited_stock:
                item.product.stock_quantity = max(0, item.product.stock_quantity - item.quantity)
            item.product.purchase_count += item.quantity
            item.product.save(update_fields=['stock_quantity', 'purchase_count'])
        
        return Response({'message': 'Payment confirmed successfully'})


# 대시보드 및 통계용 API
class DashboardStatsViewSet(viewsets.ViewSet):
    """대시보드 통계 API"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """전체 개요 통계"""
        # RWA 자산 통계
        rwa_stats = RWAAsset.objects.filter(status='active').aggregate(
            total_assets=Count('id'),
            total_value_usd=Sum('total_value_usd') or Decimal('0'),
            total_invested_glib=Sum('total_invested_glib') or Decimal('0'),
            average_apy=Avg('expected_apy') or Decimal('0'),
            total_investors=Sum('investor_count') or 0
        )
        rwa_stats['active_assets'] = rwa_stats['total_assets']
        
        # 사용자 투자 통계
        user_investments = Investment.objects.filter(
            investor=request.user,
            status__in=['confirmed', 'active', 'completed']
        )
        
        user_stats = user_investments.aggregate(
            total_invested=Sum('amount_glib') or Decimal('0'),
            total_current_value=Sum('current_value_glib') or Decimal('0'),
            active_count=Count('id', filter=Q(status='active')),
            completed_count=Count('id', filter=Q(status='completed'))
        )
        
        user_profit_loss = user_stats['total_current_value'] - user_stats['total_invested']
        user_profit_percentage = (
            (user_profit_loss / user_stats['total_invested'] * 100) 
            if user_stats['total_invested'] > 0 else Decimal('0')
        )
        
        user_stats.update({
            'total_profit_loss': user_profit_loss,
            'profit_loss_percentage': user_profit_percentage,
            'active_investments_count': user_stats.pop('active_count'),
            'completed_investments_count': user_stats.pop('completed_count')
        })
        
        # 쇼핑몰 통계
        shopping_stats = {
            'total_products': ShoppingProduct.objects.filter(status='active').count(),
            'featured_products': ShoppingProduct.objects.filter(status='active', is_featured=True).count(),
            'user_orders': ShoppingOrder.objects.filter(customer=request.user).count(),
            'pending_orders': ShoppingOrder.objects.filter(customer=request.user, status='pending').count()
        }
        
        return Response({
            'rwa_stats': RWAAssetStatsSerializer(rwa_stats).data,
            'investment_stats': InvestmentStatsSerializer(user_stats).data,
            'shopping_stats': shopping_stats
        })


class UserProfileViewSet(viewsets.ViewSet):
    """사용자 프로필 API"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'], url_path='profile')
    def get_profile(self, request):
        """사용자 프로필 조회"""
        user = request.user
        
        # 사용자 기본 정보
        profile_data = {
            'id': str(user.id),
            'email': user.email,
            'username': user.username,
            'wallet_address': getattr(user, 'wallet_address', ''),
            'name': getattr(user, 'name', ''),
            'phone': getattr(user, 'phone', ''),
            'profile_image': getattr(user, 'profile_image', ''),
            'role': getattr(user, 'role', 'user'),
            'is_active': user.is_active,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
        }
        
        # 투자 통계 추가
        investments = Investment.objects.filter(investor=user)
        investment_stats = investments.aggregate(
            total_invested=Sum('amount_glib') or Decimal('0'),
            total_current_value=Sum('current_value_glib') or Decimal('0'),
            active_count=Count('id', filter=Q(status='active')),
            completed_count=Count('id', filter=Q(status='completed'))
        )
        
        profit_loss = investment_stats['total_current_value'] - investment_stats['total_invested']
        profit_percentage = (
            (profit_loss / investment_stats['total_invested'] * 100) 
            if investment_stats['total_invested'] > 0 else Decimal('0')
        )
        
        profile_data['investment_stats'] = {
            'total_invested': str(investment_stats['total_invested']),
            'total_current_value': str(investment_stats['total_current_value']),
            'total_profit_loss': str(profit_loss),
            'profit_loss_percentage': str(profit_percentage),
            'active_investments': investment_stats['active_count'],
            'completed_investments': investment_stats['completed_count']
        }
        
        return Response(profile_data)
    
    @action(detail=False, methods=['patch'], url_path='profile')
    def update_profile(self, request):
        """사용자 프로필 수정"""
        user = request.user
        data = request.data
        
        # 업데이트 가능한 필드들
        updatable_fields = ['name', 'phone', 'profile_image']
        updated_fields = []
        
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
                updated_fields.append(field)
        
        if updated_fields:
            user.save(update_fields=updated_fields)
        
        return self.get_profile(request)