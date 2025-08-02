from django.core.management.base import BaseCommand
from apps.gli_content.models import (
    BusinessContent, ShoppingCategory, ShoppingProduct, 
    RWACategory, RWAAsset, Investment
)
from apps.solana_auth.models import SolanaUser
from decimal import Decimal
from datetime import datetime, timedelta
import uuid


class Command(BaseCommand):
    help = 'Create seed data for GLI content models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of data (delete existing)',
        )

    def handle(self, *args, **options):
        if options['force']:
            self.stdout.write('Deleting existing data...')
            BusinessContent.objects.all().delete()
            ShoppingCategory.objects.all().delete()
            ShoppingProduct.objects.all().delete()
            RWACategory.objects.all().delete()
            RWAAsset.objects.all().delete()
            Investment.objects.all().delete()

        self.create_business_content()
        self.create_shopping_data()
        self.create_rwa_data()
        self.create_sample_investments()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Successfully created seed data!')
        )

    def create_business_content(self):
        """사업소개 콘텐츠 생성"""
        self.stdout.write('Creating business content...')
        
        business_contents = [
            {
                'section': 'background',
                'title': 'GLI 플랫폼 소개',
                'subtitle': '혁신적인 Web3 레저투자 생태계',
                'content': 'GLI는 블록체인 기술을 기반으로 한 혁신적인 Web3 레저투자 플랫폼입니다. 사용자들이 안전하고 투명한 환경에서 다양한 투자 기회를 탐색하고 참여할 수 있도록 지원합니다.',
                'image_url': 'https://example.com/images/gli-intro.jpg',
                'order': 1,
            },
            {
                'section': 'team',
                'title': '핵심 사업 영역',
                'subtitle': 'RWA 투자 및 토큰 생태계',
                'content': '실물 자산(RWA) 투자, 토큰 경제, 스테이킹 서비스 등 다양한 Web3 금융 서비스를 제공하여 전통 금융과 DeFi의 장점을 결합합니다.',
                'image_url': 'https://example.com/images/business-areas.jpg',
                'order': 1,
            },
            {
                'section': 'strategy',
                'title': '투자 전략',
                'subtitle': '안전하고 수익성 높은 투자',
                'content': '철저한 리스크 관리와 전문적인 자산 분석을 통해 안정적이면서도 높은 수익을 창출할 수 있는 투자 기회를 제공합니다.',
                'image_url': 'https://example.com/images/strategy.jpg',
                'order': 1,
            },
            {
                'section': 'roadmap',
                'title': 'GLI 생태계 토큰',
                'subtitle': 'GLIB, GLIL, GLID 토큰 시스템',
                'content': 'GLIB(기본 토큰), GLIL(레저 토큰), GLID(투자 토큰)로 구성된 다층 토큰 시스템으로 다양한 사용자 니즈에 대응합니다.',
                'image_url': 'https://example.com/images/tokens.jpg',
                'order': 1,
            },
            {
                'section': 'tokens',
                'title': '주요 추진 사업',
                'subtitle': '2024-2025 로드맵',
                'content': 'RWA 투자 상품 확대, 글로벌 파트너십 구축, AI 기반 투자 자문 서비스 런칭 등 혁신적인 서비스들을 단계적으로 출시할 예정입니다.',
                'image_url': 'https://example.com/images/roadmap.jpg',
                'order': 1,
            }
        ]

        for content_data in business_contents:
            BusinessContent.objects.get_or_create(
                section=content_data['section'],
                order=content_data['order'],
                defaults=content_data
            )

    def create_shopping_data(self):
        """쇼핑몰 데이터 생성"""
        self.stdout.write('Creating shopping data...')
        
        # 카테고리 생성
        categories_data = [
            {'name': '럭셔리 굿즈', 'description': '고급 명품 및 컬렉션', 'icon': '💎', 'order': 1},
            {'name': '리조트 예약', 'description': '프리미엄 리조트 및 호텔', 'icon': '🏖️', 'order': 2},
            {'name': '레스토랑', 'description': '파인다이닝 레스토랑 예약', 'icon': '🍽️', 'order': 3},
            {'name': '프리미엄 서비스', 'description': '개인 맞춤 서비스', 'icon': '⭐', 'order': 4},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = ShoppingCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category

        # 상품 생성
        products_data = [
            {
                'category': categories['럭셔리 굿즈'],
                'name': '로렉스 서브마리너',
                'description': '클래식한 다이빙 워치의 아이콘',
                'short_description': '프리미엄 스위스 시계',
                'product_type': 'goods',
                'price_glil': Decimal('25000'),
                'price_usd': Decimal('8500.00'),
                'stock_quantity': 5,
                'main_image_url': 'https://example.com/images/rolex.jpg',
                'is_featured': True,
                'tags': ['시계', '럭셔리', '스위스', '다이빙'],
            },
            {
                'category': categories['리조트 예약'],
                'name': '몰디브 프리미엄 리조트 3박4일',
                'description': '프라이빗 풀빌라에서 즐기는 럭셔리 휴양',
                'short_description': '몰디브 올인클루시브 패키지',
                'product_type': 'resort',
                'price_glil': Decimal('15000'),
                'price_usd': Decimal('5200.00'),
                'unlimited_stock': True,
                'main_image_url': 'https://example.com/images/maldives.jpg',
                'is_featured': True,
                'tags': ['몰디브', '리조트', '풀빌라', '올인클루시브'],
            },
            {
                'category': categories['레스토랑'],
                'name': '미슐랭 3스타 레스토랑 디너',
                'description': '세계적인 셰프의 시그니처 코스 메뉴',
                'short_description': '프리미엄 파인다이닝 경험',
                'product_type': 'restaurant',
                'price_glil': Decimal('800'),
                'price_usd': Decimal('280.00'),
                'stock_quantity': 20,
                'main_image_url': 'https://example.com/images/michelin.jpg',
                'tags': ['미슐랭', '파인다이닝', '코스요리'],
            }
        ]

        for product_data in products_data:
            ShoppingProduct.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )

    def create_rwa_data(self):
        """RWA 투자 자산 데이터 생성"""
        self.stdout.write('Creating RWA data...')
        
        # RWA 카테고리 생성
        rwa_categories_data = [
            {'name': '부동산', 'description': '상업용 및 주거용 부동산', 'icon': '🏢', 'order': 1},
            {'name': '원자재', 'description': '금, 은, 구리 등 귀금속', 'icon': '🥇', 'order': 2},
            {'name': '아트 & 컬렉션', 'description': '미술품 및 희귀 수집품', 'icon': '🎨', 'order': 3},
            {'name': '인프라', 'description': '에너지 및 인프라 프로젝트', 'icon': '⚡', 'order': 4},
        ]

        rwa_categories = {}
        for cat_data in rwa_categories_data:
            category, created = RWACategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            rwa_categories[cat_data['name']] = category

        # RWA 자산 생성
        rwa_assets_data = [
            {
                'category': rwa_categories['부동산'],
                'name': '서울 강남구 프리미엄 오피스텔',
                'description': '강남구 테헤란로 인근 신축 오피스텔 투자 상품입니다. 임대 수익률과 자본 증식을 동시에 추구할 수 있습니다.',
                'short_description': '강남 테헤란로 신축 오피스텔',
                'total_value_usd': Decimal('2500000.00'),
                'min_investment_gleb': Decimal('1000'),
                'max_investment_gleb': Decimal('100000'),
                'expected_apy': Decimal('8.5'),
                'risk_level': 'medium',
                'investment_period_months': 36,
                'lock_period_months': 12,
                'asset_location': '서울특별시 강남구',
                'asset_type': '상업용 부동산',
                'funding_target_gleb': Decimal('800000'),
                'is_featured': True,
            },
            {
                'category': rwa_categories['원자재'],
                'name': '골드 ETF 포트폴리오',
                'description': '다양한 금 ETF로 구성된 포트폴리오로 인플레이션 헤지 효과를 제공합니다.',
                'short_description': '분산 투자된 금 ETF 상품',
                'total_value_usd': Decimal('1000000.00'),
                'min_investment_gleb': Decimal('500'),
                'max_investment_gleb': Decimal('50000'),
                'expected_apy': Decimal('6.2'),
                'risk_level': 'low',
                'investment_period_months': 24,
                'lock_period_months': 6,
                'asset_location': '글로벌',
                'asset_type': '귀금속 ETF',
                'funding_target_gleb': Decimal('320000'),
                'is_featured': True,
            },
            {
                'category': rwa_categories['아트 & 컬렉션'],
                'name': '현대미술 컬렉션 펀드',
                'description': '신진 및 중견 작가들의 작품으로 구성된 미술품 투자 펀드입니다.',
                'short_description': '현대미술 작품 투자 포트폴리오',
                'total_value_usd': Decimal('800000.00'),
                'min_investment_gleb': Decimal('2000'),
                'max_investment_gleb': Decimal('80000'),
                'expected_apy': Decimal('12.3'),
                'risk_level': 'high',
                'investment_period_months': 60,
                'lock_period_months': 24,
                'asset_location': '한국, 미국, 유럽',
                'asset_type': '미술품',
                'funding_target_gleb': Decimal('256000'),
            }
        ]

        for asset_data in rwa_assets_data:
            RWAAsset.objects.get_or_create(
                name=asset_data['name'],
                defaults=asset_data
            )

    def create_sample_investments(self):
        """샘플 투자 내역 생성"""
        self.stdout.write('Creating sample investments...')
        
        # 테스트 사용자 가져오기
        try:
            user = SolanaUser.objects.get(email='user@gli.com')
        except SolanaUser.DoesNotExist:
            self.stdout.write('Test user not found, skipping investment creation')
            return

        # RWA 자산 가져오기
        rwa_assets = RWAAsset.objects.all()
        if not rwa_assets.exists():
            self.stdout.write('No RWA assets found, skipping investment creation')
            return

        # 샘플 투자 생성
        sample_investments = [
            {
                'investor': user,
                'rwa_asset': rwa_assets.first(),
                'amount_gleb': Decimal('5000'),
                'amount_usd_at_time': Decimal('1750.00'),
                'expected_return_date': datetime.now() + timedelta(days=1095),  # 3년
                'expected_apy_at_time': Decimal('8.5'),
                'current_value_gleb': Decimal('5425'),  # 8.5% 수익
                'status': 'active',
            }
        ]

        for investment_data in sample_investments:
            Investment.objects.get_or_create(
                investor=investment_data['investor'],
                rwa_asset=investment_data['rwa_asset'],
                defaults=investment_data
            )