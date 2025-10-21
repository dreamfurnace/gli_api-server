from django.core.management.base import BaseCommand
from apps.gli_content.models import RWACategory, RWAAsset
from decimal import Decimal


class Command(BaseCommand):
    help = '아시아 지역 RWA 투자 자산 10개 생성'

    def handle(self, *args, **options):
        self.stdout.write('아시아 RWA 자산 데이터 생성 시작...')

        # 카테고리 생성
        categories_data = [
            {'name': '부동산', 'icon': '🏢', 'description': '실물 부동산 투자', 'order': 1},
            {'name': '카지노', 'icon': '🎰', 'description': '카지노 및 복합 리조트', 'order': 2},
            {'name': '사업 아이템', 'icon': '💼', 'description': '프랜차이즈 및 사업 투자', 'order': 3},
            {'name': '농업', 'icon': '🌾', 'description': '농업 및 생산형 자산', 'order': 4},
            {'name': '레저', 'icon': '⛱️', 'description': '레저 및 휴양 시설', 'order': 5},
            {'name': '브랜드', 'icon': '🏷️', 'description': '브랜드 및 콘텐츠 사업', 'order': 6},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = RWACategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'order': cat_data['order'],
                    'is_active': True
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ 카테고리 생성: {category.name}'))

        # RWA 자산 데이터
        assets_data = [
            {
                'category': '부동산',
                'name': '캄보디아 시아누크빌 Star Bay 리조트',
                'name_en': 'Star Bay Resort, Sihanoukville, Cambodia',
                'asset_type': '리조트',
                'asset_type_en': 'Resort',
                'expected_apy': Decimal('11.2'),
                'risk_level': 'medium',
                'asset_location': '캄보디아 시아누크빌 해안도로 인근',
                'asset_location_en': 'Near coastal road, Sihanoukville, Cambodia',
                'min_investment_glib': Decimal('200.00000000'),
                'total_value_usd': Decimal('8000000.00'),
                'short_description': '캄보디아의 신흥 휴양지에 위치한 해안 리조트로, 안정적인 관광 수익 창출이 가능합니다.',
                'short_description_en': 'A beachfront resort in Cambodia\'s emerging coastal city, generating stable tourism revenue.',
                'description': '''시아누크빌 중심 해안도로에 위치

주요 특징:
- 평균 객실 점유율 82%
- 현지 정부 관광 인센티브 대상
- 연평균 수익률 10~12% 예상

투자 포인트:
1. 캄보디아 신흥 휴양 도시의 성장 잠재력
2. 중국 및 아시아 관광객 증가 추세
3. 정부 관광 인센티브 혜택
4. 안정적인 해안 리조트 운영''',
                'description_en': '''Located along Sihanoukville's main coastal road

Key Features:
- 82% average occupancy rate
- Eligible for local government tourism incentives
- Expected annual yield: 10–12%

Investment Highlights:
1. Growth potential in Cambodia's emerging resort city
2. Increasing Chinese and Asian tourist arrivals
3. Government tourism incentive benefits
4. Stable beachfront resort operations''',
                'investment_period_months': 36,
                'lock_period_months': 12,
                'is_featured': True,
                'area_sqm': Decimal('8500.00'),
                'operation_type': 'consignment',
            },
            {
                'category': '부동산',
                'name': '호이안 리조트 & 골프',
                'name_en': 'Hoi An Resort & Golf',
                'asset_type': '리조트',
                'asset_type_en': 'Resort',
                'expected_apy': Decimal('10.8'),
                'risk_level': 'medium',
                'asset_location': '베트남 꽝남성 호이안 해변 인근',
                'asset_location_en': 'Near Hoi An Beach, Quang Nam, Vietnam',
                'min_investment_glib': Decimal('300.00000000'),
                'total_value_usd': Decimal('10000000.00'),
                'short_description': '베트남 중부의 명소 호이안에 위치한 프리미엄 리조트 & 골프 클럽입니다.',
                'short_description_en': 'A premium resort and golf club located in the central Vietnamese city of Hoi An.',
                'description': '''베트남 중부 호이안 해변 인근 프리미엄 리조트

주요 특징:
- 18홀 챔피언십 골프 코스
- 외국인 관광객 비중 70% 이상
- 안정적 숙박·그린피 수익

투자 포인트:
1. 유네스코 세계문화유산 도시 인근
2. 골프 관광 복합 시설
3. 높은 외국인 관광객 비중
4. 다변화된 수익 구조''',
                'description_en': '''Premium resort near Hoi An Beach, Central Vietnam

Key Features:
- 18-hole championship golf course
- 70% foreign visitor ratio
- Stable income from lodging and golf fees

Investment Highlights:
1. Near UNESCO World Heritage city
2. Golf tourism complex facility
3. High proportion of international tourists
4. Diversified revenue streams''',
                'investment_period_months': 36,
                'lock_period_months': 12,
                'is_featured': True,
                'area_sqm': Decimal('15000.00'),
                'operation_type': 'consignment',
            },
            {
                'category': '부동산',
                'name': '호치민 ERA 부동산',
                'name_en': 'ERA Real Estate, Ho Chi Minh City',
                'asset_type': '상업용',
                'asset_type_en': 'Commercial',
                'expected_apy': Decimal('9.5'),
                'risk_level': 'medium',
                'asset_location': '호치민 7군 푸미흥 비즈니스 지구',
                'asset_location_en': 'Phu My Hung Business District, District 7, Ho Chi Minh',
                'min_investment_glib': Decimal('150.00000000'),
                'total_value_usd': Decimal('6000000.00'),
                'short_description': '호치민 신흥 비즈니스 지구의 오피스 빌딩 투자 프로젝트입니다.',
                'short_description_en': 'Office property investment in the emerging Phu My Hung business district.',
                'description': '''호치민 7군 푸미흥 비즈니스 지구 오피스 투자

주요 특징:
- 신흥 비즈니스 지구 중심 입지
- 외국계 기업 임차인 다수
- 안정적인 임대 수익 구조

투자 포인트:
1. 호치민 경제 성장 수혜
2. 외국계 기업 수요 증가
3. 안정적인 상업용 부동산
4. 장기 임대 계약 기반''',
                'description_en': '''Office investment in Phu My Hung District 7, HCMC

Key Features:
- Prime location in emerging business district
- Multiple foreign corporate tenants
- Stable rental income structure

Investment Highlights:
1. Benefits from HCMC economic growth
2. Increasing foreign corporate demand
3. Stable commercial real estate
4. Long-term lease agreements''',
                'investment_period_months': 36,
                'lock_period_months': 12,
                'is_featured': False,
                'area_sqm': Decimal('4500.00'),
                'operation_type': 'rental',
            },
            {
                'category': '부동산',
                'name': '마닐라 Vista Land 부동산',
                'name_en': 'Vista Land Property, Manila',
                'asset_type': '주거용',
                'asset_type_en': 'Residential',
                'expected_apy': Decimal('8.7'),
                'risk_level': 'low',
                'asset_location': '필리핀 마닐라 Bonifacio Global City 인근',
                'asset_location_en': 'Near Bonifacio Global City, Manila, Philippines',
                'min_investment_glib': Decimal('100.00000000'),
                'total_value_usd': Decimal('4000000.00'),
                'short_description': '안정적인 임대 수익을 창출하는 중고급 주거 프로젝트입니다.',
                'short_description_en': 'Mid-to-high-end residential project generating steady rental yields.',
                'description': '''마닐라 BGC 인근 중고급 주거용 부동산

주요 특징:
- 안정적인 임대 수익 구조
- 중산층 및 외국인 거주자 타깃
- 낮은 위험도의 안정형 자산

투자 포인트:
1. BGC 비즈니스 지구 인접
2. 안정적인 주거 수요
3. 낮은 공실률
4. 보수적 투자자에 적합''',
                'description_en': '''Mid-to-high-end residential property near BGC Manila

Key Features:
- Stable rental income structure
- Targeting middle class and expat residents
- Low-risk stable asset

Investment Highlights:
1. Adjacent to BGC business district
2. Stable residential demand
3. Low vacancy rate
4. Suitable for conservative investors''',
                'investment_period_months': 36,
                'lock_period_months': 12,
                'is_featured': False,
                'area_sqm': Decimal('3200.00'),
                'operation_type': 'rental',
            },
            {
                'category': '카지노',
                'name': '세부 Waterfront Hotel & Casino',
                'name_en': 'Waterfront Hotel & Casino, Cebu',
                'asset_type': '호텔형',
                'asset_type_en': 'Hotel',
                'expected_apy': Decimal('13.2'),
                'risk_level': 'medium',
                'asset_location': '필리핀 세부 IT Park 인근',
                'asset_location_en': 'Near IT Park, Cebu, Philippines',
                'min_investment_glib': Decimal('500.00000000'),
                'total_value_usd': Decimal('12000000.00'),
                'short_description': '세부 최대 복합 카지노 리조트 중 하나로, 관광객 유입이 급증하고 있습니다.',
                'short_description_en': 'One of Cebu\'s largest integrated casino resorts with growing tourist influx.',
                'description': '''세부 대표 복합 카지노 리조트

주요 특징:
- 호텔, 카지노, 레스토랑 복합 운영
- 관광객 유입 급증 지역
- 연평균 13% 이상 수익률 예상

투자 포인트:
1. 필리핀 제2의 도시 세부 입지
2. 복합 엔터테인먼트 시설
3. 높은 수익률 잠재력
4. 관광산업 성장 수혜''',
                'description_en': '''Leading integrated casino resort in Cebu

Key Features:
- Hotel, casino, restaurant complex
- Growing tourist destination
- Expected annual yield above 13%

Investment Highlights:
1. Located in Cebu, Philippines' 2nd largest city
2. Integrated entertainment facility
3. High yield potential
4. Tourism industry growth benefits''',
                'investment_period_months': 36,
                'lock_period_months': 12,
                'is_featured': True,
                'area_sqm': Decimal('18000.00'),
                'operation_type': 'consignment',
            },
            {
                'category': '사업 아이템',
                'name': 'Brown Coffee 프랜차이즈',
                'name_en': 'Brown Coffee Franchise Cambodia',
                'asset_type': '프랜차이즈',
                'asset_type_en': 'Franchise',
                'expected_apy': Decimal('14.0'),
                'risk_level': 'medium',
                'asset_location': '프놈펜, 캄보디아',
                'asset_location_en': 'Phnom Penh, Cambodia',
                'min_investment_glib': Decimal('100.00000000'),
                'total_value_usd': Decimal('3500000.00'),
                'short_description': '캄보디아 대표 커피 브랜드 Brown의 신규 매장 투자형 프랜차이즈입니다.',
                'short_description_en': 'Investment franchise for Brown, Cambodia\'s leading coffee brand.',
                'description': '''캄보디아 1위 커피 브랜드 프랜차이즈

주요 특징:
- 현지 시장 점유율 1위
- 신규 매장 투자형 모델
- 안정적인 프랜차이즈 수익

투자 포인트:
1. 캄보디아 커피 시장 성장
2. 검증된 브랜드 파워
3. 프랜차이즈 수익 분배 모델
4. 비교적 낮은 투자금''',
                'description_en': '''Cambodia's #1 coffee brand franchise

Key Features:
- Market leader in Cambodia
- New store investment model
- Stable franchise revenue

Investment Highlights:
1. Growing coffee market in Cambodia
2. Proven brand power
3. Franchise revenue sharing model
4. Relatively low investment amount''',
                'investment_period_months': 36,
                'lock_period_months': 12,
                'is_featured': False,
                'area_sqm': Decimal('150.00'),
                'operation_type': 'direct',
            },
            {
                'category': '농업',
                'name': '말레이시아 두리안 농장 RWA 프로젝트',
                'name_en': 'Durian Farm RWA Project, Malaysia',
                'asset_type': '생산형',
                'asset_type_en': 'Production',
                'expected_apy': Decimal('15.0'),
                'risk_level': 'high',
                'asset_location': '말레이시아 파항주',
                'asset_location_en': 'Pahang, Malaysia',
                'min_investment_glib': Decimal('80.00000000'),
                'total_value_usd': Decimal('2800000.00'),
                'short_description': '고급 두리안 수출용 농장에 대한 수익 분배형 투자입니다.',
                'short_description_en': 'Revenue-sharing investment in export-grade durian farm.',
                'description': '''말레이시아 프리미엄 두리안 농장 투자

주요 특징:
- 고급 무산왕(Musang King) 품종
- 중국 수출 중심 판로
- 수확 기반 수익 분배

투자 포인트:
1. 중국 두리안 수요 급증
2. 프리미엄 품종 생산
3. 높은 수익률 가능성
4. 농업 자산 다변화

리스크:
- 기후 및 작황 변동성
- 수출 규제 변화 가능성''',
                'description_en': '''Premium durian farm investment in Malaysia

Key Features:
- Premium Musang King variety
- China export-focused distribution
- Harvest-based revenue sharing

Investment Highlights:
1. Surging durian demand in China
2. Premium variety production
3. High yield potential
4. Agricultural asset diversification

Risks:
- Climate and crop volatility
- Potential export regulation changes''',
                'investment_period_months': 48,
                'lock_period_months': 24,
                'is_featured': False,
                'area_sqm': Decimal('25000.00'),
                'operation_type': 'consignment',
            },
            {
                'category': '레저',
                'name': '세부 RYOUKU 고급 일식 리조트',
                'name_en': 'RYOUKU Japanese Resort, Cebu',
                'asset_type': '리조트',
                'asset_type_en': 'Resort',
                'expected_apy': Decimal('12.5'),
                'risk_level': 'medium',
                'asset_location': '필리핀 세부 막탄섬 해안',
                'asset_location_en': 'Mactan Island Coast, Cebu, Philippines',
                'min_investment_glib': Decimal('300.00000000'),
                'total_value_usd': Decimal('9000000.00'),
                'short_description': '일본 프랜차이즈와 제휴한 세부 고급 레저 리조트 프로젝트입니다.',
                'short_description_en': 'A premium Japanese-branded resort project located on Cebu\'s Mactan Island.',
                'description': '''일본식 프리미엄 레저 리조트

주요 특징:
- 일본 브랜드 제휴 운영
- 막탄섬 해안 프라임 입지
- 일본식 온천 및 스파 시설

투자 포인트:
1. 일본 관광객 타깃
2. 프리미엄 브랜드 파워
3. 차별화된 일본식 서비스
4. 막탄섬 관광 허브 입지''',
                'description_en': '''Japanese-style premium leisure resort

Key Features:
- Japanese brand partnership
- Prime Mactan Island beachfront location
- Japanese-style onsen and spa facilities

Investment Highlights:
1. Targeting Japanese tourists
2. Premium brand power
3. Differentiated Japanese-style service
4. Mactan Island tourism hub location''',
                'investment_period_months': 36,
                'lock_period_months': 12,
                'is_featured': True,
                'area_sqm': Decimal('12000.00'),
                'operation_type': 'consignment',
            },
            {
                'category': '브랜드',
                'name': 'Xijiu 싱가포르 브랜드 콘텐츠 투자',
                'name_en': 'Xijiu Brand Content Investment, Singapore',
                'asset_type': '콘텐츠',
                'asset_type_en': 'Content',
                'expected_apy': Decimal('10.0'),
                'risk_level': 'medium',
                'asset_location': '싱가포르 Marina Bay',
                'asset_location_en': 'Marina Bay, Singapore',
                'min_investment_glib': Decimal('150.00000000'),
                'total_value_usd': Decimal('5500000.00'),
                'short_description': '중국 명주 Xijiu 브랜드의 글로벌 라이프스타일 콘텐츠 사업 투자.',
                'short_description_en': 'Investment in global lifestyle brand expansion of China\'s Xijiu liquor company.',
                'description': '''Xijiu 글로벌 브랜드 콘텐츠 사업

주요 특징:
- 중국 명주 브랜드 글로벌 확장
- 싱가포르 허브 라이프스타일 콘텐츠
- 브랜드 마케팅 수익 배당

투자 포인트:
1. 중국 명품 주류 브랜드
2. 동남아 시장 진출 전략
3. 콘텐츠 및 브랜딩 수익
4. 라이프스타일 비즈니스 확장''',
                'description_en': '''Xijiu global brand content business

Key Features:
- Global expansion of Chinese premium liquor brand
- Singapore-based lifestyle content hub
- Brand marketing revenue distribution

Investment Highlights:
1. Chinese luxury liquor brand
2. Southeast Asia market entry strategy
3. Content and branding revenue
4. Lifestyle business expansion''',
                'investment_period_months': 36,
                'lock_period_months': 12,
                'is_featured': False,
                'area_sqm': Decimal('800.00'),
                'operation_type': 'other',
            },
            {
                'category': '카지노',
                'name': '마카오 Sands Group 카지노 지분 참여',
                'name_en': 'Sands Group Casino Equity, Macau',
                'asset_type': '지분형',
                'asset_type_en': 'Equity',
                'expected_apy': Decimal('16.3'),
                'risk_level': 'high',
                'asset_location': '마카오 Cotai Strip',
                'asset_location_en': 'Cotai Strip, Macau',
                'min_investment_glib': Decimal('1000.00000000'),
                'total_value_usd': Decimal('20000000.00'),
                'short_description': '마카오 최대 카지노 그룹의 지분형 RWA 프로젝트입니다.',
                'short_description_en': 'Equity-based RWA project in Macau\'s leading casino group.',
                'description': '''마카오 대표 카지노 그룹 지분 투자

주요 특징:
- Sands Group 지분 참여형
- 코타이 스트립 프라임 입지
- 고수익 고위험 구조

투자 포인트:
1. 세계 최대 카지노 시장 마카오
2. 업계 1위 그룹 지분 투자
3. 높은 수익률 가능성
4. 중국 관광객 회복 수혜

리스크:
- 규제 변화 리스크
- 경기 민감도 높음
- 최소 투자금 상대적 고액''',
                'description_en': '''Equity investment in Macau's leading casino group

Key Features:
- Sands Group equity participation
- Prime Cotai Strip location
- High-risk high-return structure

Investment Highlights:
1. Macau, world's largest casino market
2. Industry leader equity investment
3. High yield potential
4. Chinese tourist recovery benefits

Risks:
- Regulatory change risks
- High economic sensitivity
- Relatively high minimum investment''',
                'investment_period_months': 48,
                'lock_period_months': 24,
                'is_featured': True,
                'area_sqm': Decimal('50000.00'),
                'operation_type': 'other',
            },
        ]

        # 자산 생성
        created_count = 0
        for asset_data in assets_data:
            category = categories[asset_data.pop('category')]
            asset_data['category'] = category
            asset_data['status'] = 'active'
            asset_data['max_investment_glib'] = asset_data['total_value_usd'] / 100  # 총 가치의 1%

            asset, created = RWAAsset.objects.get_or_create(
                name=asset_data['name'],
                defaults=asset_data
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ RWA 자산 생성: {asset.name}'))
                self.stdout.write(f'   - 카테고리: {asset.category.name}')
                self.stdout.write(f'   - 위치: {asset.asset_location}')
                self.stdout.write(f'   - 예상 APY: {asset.expected_apy}%')
                self.stdout.write(f'   - 최소 투자: {asset.min_investment_glib} GLIB')
                self.stdout.write(f'   - 위험도: {asset.get_risk_level_display()}')
            else:
                self.stdout.write(f'ℹ️ RWA 자산 이미 존재: {asset.name}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ 총 {created_count}개의 새로운 자산이 생성되었습니다!'))
        self.stdout.write(f'\n관리자 페이지에서 확인: http://localhost:3001/rwa/assets')
        self.stdout.write(f'사용자 페이지에서 확인: http://localhost:3000/rwa-assets')
