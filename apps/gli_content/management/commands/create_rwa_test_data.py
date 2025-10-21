from django.core.management.base import BaseCommand
from apps.gli_content.models import RWACategory, RWAAsset
from decimal import Decimal


class Command(BaseCommand):
    help = 'RWA 투자 자산 테스트 데이터 생성'

    def handle(self, *args, **options):
        self.stdout.write('RWA 테스트 데이터 생성 시작...')

        # 카테고리 생성
        category, created = RWACategory.objects.get_or_create(
            name='부동산',
            defaults={
                'description': '실물 부동산 투자',
                'icon': '🏢',
                'order': 1,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ 카테고리 생성: {category.name}'))
        else:
            self.stdout.write(f'ℹ️ 카테고리 이미 존재: {category.name}')

        # 제주도 리조트 자산 생성
        asset_data = {
            'category': category,
            'name': '제주도 프리미엄 리조트',
            'name_en': 'Jeju Premium Resort',
            'description': '''제주도 서귀포시에 위치한 프리미엄 리조트입니다.

주요 특징:
- 오션뷰가 보이는 50개의 객실
- 연중 높은 객실 점유율 (평균 85%)
- 안정적인 임대 수익 구조
- 연 8-12% 수익률 예상

투자 포인트:
1. 제주도 관광객 증가 추세
2. 프리미엄 숙박 시설 수요 증가
3. 전문 운영사의 위탁 운영
4. 분기별 배당 지급

리스크:
- 계절적 수요 변동
- 관광객 수 변화에 따른 수익률 변동
- 시설 유지보수 비용

본 자산은 GLI-B 토큰으로 투자 가능하며, 최소 투자금액은 100 GLIB입니다.''',
            'description_en': '''A premium resort located in Seogwipo, Jeju Island.

Key Features:
- 50 ocean-view rooms
- High year-round occupancy rate (avg. 85%)
- Stable rental income structure
- Expected return: 8-12% annually

Investment Highlights:
1. Growing tourism in Jeju Island
2. Increasing demand for premium accommodation
3. Professional management by experienced operator
4. Quarterly dividend distribution

Risks:
- Seasonal demand fluctuation
- Revenue volatility based on tourist numbers
- Facility maintenance costs

This asset can be invested with GLI-B tokens, with a minimum investment of 100 GLIB.''',
            'short_description': '제주도 서귀포 오션뷰 프리미엄 리조트, 연 8-12% 수익률',
            'short_description_en': 'Jeju Seogwipo Ocean View Premium Resort, 8-12% Annual Return',
            'total_value_usd': Decimal('5000000.00'),  # 50억원 (약 500만 달러)
            'min_investment_glib': Decimal('100.00000000'),
            'max_investment_glib': Decimal('10000.00000000'),
            'expected_apy': Decimal('10.50'),
            'historical_returns': [
                {'year': 2023, 'return': 11.2},
                {'year': 2022, 'return': 9.8},
                {'year': 2021, 'return': 10.5}
            ],
            'risk_level': 'medium',
            'risk_factors': [
                '계절적 수요 변동',
                '관광객 수 변화',
                '환율 변동',
                '시설 노후화'
            ],
            'investment_period_months': 36,  # 3년
            'lock_period_months': 12,  # 1년 락업
            'asset_location': '제주특별자치도 서귀포시 중문관광로 72번길',
            'asset_location_en': '72-gil, Jungmun Tourism-ro, Seogwipo-si, Jeju-do, South Korea',
            'asset_type': '리조트',
            'asset_type_en': 'Resort',
            'area_sqm': Decimal('12500.50'),  # 약 3,780평
            'operation_type': 'consignment',  # 위탁 운영
            'underlying_assets': {
                'land_value': 2000000,
                'building_value': 3000000,
                'facilities': [
                    {'type': '객실', 'count': 50, 'avg_size_sqm': 45},
                    {'type': '레스토랑', 'count': 2, 'size_sqm': 300},
                    {'type': '수영장', 'count': 1, 'size_sqm': 500},
                    {'type': '스파', 'count': 1, 'size_sqm': 200}
                ]
            },
            'main_image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800',
            'image_urls': [
                'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800',
                'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800',
                'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
                'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800'
            ],
            'document_urls': [
                {'name': '투자설명서.pdf', 'url': '/documents/resort-prospectus.pdf'},
                {'name': '감정평가서.pdf', 'url': '/documents/resort-appraisal.pdf'},
                {'name': '운영계획서.pdf', 'url': '/documents/resort-operation-plan.pdf'}
            ],
            'total_invested_glib': Decimal('3500.00000000'),
            'investor_count': 12,
            'funding_target_glib': Decimal('50000.00000000'),
            'status': 'active',
            'is_featured': True,
            'metadata': {
                'operator': '제주리조트운영(주)',
                'completion_date': '2020-06-15',
                'last_renovation': '2023-01-10',
                'certifications': ['친환경 건축물 인증', '관광숙박업 등록'],
                'amenities': ['와이파이', '주차장', '조식 포함', '픽업 서비스', '해변 접근'],
                'languages': ['한국어', '영어', '중국어', '일본어']
            }
        }

        asset, created = RWAAsset.objects.get_or_create(
            name=asset_data['name'],
            defaults=asset_data
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ RWA 자산 생성: {asset.name}'))
            self.stdout.write(f'   - 위치: {asset.asset_location}')
            self.stdout.write(f'   - 면적: {asset.area_sqm}㎡')
            self.stdout.write(f'   - 예상 APY: {asset.expected_apy}%')
            self.stdout.write(f'   - 최소 투자: {asset.min_investment_glib} GLIB')
            self.stdout.write(f'   - 운영 형태: {asset.get_operation_type_display()}')
            self.stdout.write(f'   - 상태: {asset.get_status_display()}')
        else:
            self.stdout.write(f'ℹ️ RWA 자산 이미 존재: {asset.name}')

        self.stdout.write(self.style.SUCCESS('\n✅ 테스트 데이터 생성 완료!'))
        self.stdout.write(f'\n관리자 페이지에서 확인: http://localhost:3001/rwa/assets')
        self.stdout.write(f'사용자 페이지에서 확인: http://localhost:3000/rwa-assets')
