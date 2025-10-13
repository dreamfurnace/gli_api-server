from django.core.management.base import BaseCommand
from apps.solana_auth.models import DevelopmentTimeline, TokenEcosystem


class Command(BaseCommand):
    help = '사업소개 데이터 시딩 (개발 일정 및 토큰 에코시스템)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🌱 사업소개 데이터 시딩을 시작합니다...'))

        # 개발 일정 관리 데이터 시딩
        self.seed_development_timelines()

        # 토큰 에코시스템 데이터 시딩
        self.seed_token_ecosystems()

        self.stdout.write(self.style.SUCCESS('✅ 사업소개 데이터 시딩이 완료되었습니다!'))

    def seed_development_timelines(self):
        """개발 일정 관리 데이터 시딩"""
        self.stdout.write('📅 개발 일정 데이터를 생성합니다...')

        timelines = [
            {
                'quarter': '2024 Q1',
                'status_icon': '✅',
                'title_ko': '플랫폼 MVP 출시',
                'title_en': 'Platform MVP Launch',
                'description_ko': '기본 플랫폼과 토큰 시스템 출시',
                'description_en': 'Launch basic platform and token system',
                'order': 1,
                'is_active': True,
            },
            {
                'quarter': '2024 Q2',
                'status_icon': '✅',
                'title_ko': '리조트 파트너십',
                'title_en': 'Resort Partnership',
                'description_ko': '첫 번째 리조트 파트너와의 협약 체결',
                'description_en': 'Partnership agreement with first resort partner',
                'order': 2,
                'is_active': True,
            },
            {
                'quarter': '2024 Q3',
                'status_icon': '🔄',
                'title_ko': '베타 서비스',
                'title_en': 'Beta Service',
                'description_ko': '제한된 사용자 대상 베타 서비스 시작',
                'description_en': 'Start beta service for limited users',
                'order': 3,
                'is_active': True,
            },
            {
                'quarter': '2024 Q4',
                'status_icon': '⏳',
                'title_ko': '정식 서비스',
                'title_en': 'Official Service',
                'description_ko': '전체 기능을 포함한 정식 서비스 오픈',
                'description_en': 'Open official service with full features',
                'order': 4,
                'is_active': True,
            },
        ]

        for timeline_data in timelines:
            timeline, created = DevelopmentTimeline.objects.get_or_create(
                quarter=timeline_data['quarter'],
                defaults=timeline_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✅ 생성됨: {timeline.quarter} - {timeline.title_ko}'))
            else:
                self.stdout.write(f'  ⏭️  이미 존재: {timeline.quarter} - {timeline.title_ko}')

    def seed_token_ecosystems(self):
        """토큰 에코시스템 데이터 시딩"""
        self.stdout.write('🪙 토큰 에코시스템 데이터를 생성합니다...')

        tokens = [
            {
                'icon': '🔵',
                'name': 'GLI Business',
                'symbol': 'GLIB',
                'description_ko': 'GLI 플랫폼의 핵심 비즈니스 토큰으로, 리조트 예약, NFT 거래, 스테이킹 보상 등에 사용됩니다.',
                'description_en': 'The core business token of the GLI platform, used for resort reservations, NFT transactions, staking rewards, and more.',
                'features': [
                    '리조트 예약 및 결제',
                    '스테이킹 보상 참여',
                    'NFT 마켓플레이스 거래',
                    '거버넌스 투표 참여',
                ],
                'total_supply': '100,000,000 GLIB',
                'current_price': '$0.25',
                'order': 1,
                'is_active': True,
            },
            {
                'icon': '🟣',
                'name': 'GLI DeFi',
                'symbol': 'GLID',
                'description_ko': 'DeFi 생태계를 위한 토큰으로, 유동성 제공, 렌딩, 스왑 등 다양한 DeFi 서비스에 활용됩니다.',
                'description_en': 'Token for the DeFi ecosystem, used for liquidity provision, lending, swapping, and various DeFi services.',
                'features': [
                    '유동성 풀 참여',
                    '렌딩 프로토콜 이용',
                    '자동화된 수익 농장',
                    'DEX 스왑 수수료 할인',
                ],
                'total_supply': '500,000,000 GLID',
                'current_price': '$0.08',
                'order': 2,
                'is_active': True,
            },
            {
                'icon': '🟢',
                'name': 'GLI Luxury',
                'symbol': 'GLIL',
                'description_ko': '럭셔리 서비스 전용 토큰으로, 프리미엄 리조트 이용, 고급 NFT 구매, VIP 혜택 등에 사용됩니다.',
                'description_en': 'Luxury service token for premium resort usage, high-end NFT purchases, VIP benefits, and more.',
                'features': [
                    '프리미엄 리조트 예약',
                    '럭셔리 NFT 컬렉션',
                    'VIP 멤버십 혜택',
                    '프라이빗 이벤트 참여',
                ],
                'total_supply': '10,000,000 GLIL',
                'current_price': '$2.50',
                'order': 3,
                'is_active': True,
            },
            {
                'icon': '🟡',
                'name': 'Tether USD',
                'symbol': 'USDT',
                'description_ko': '안정적인 가치 저장 수단으로, GLI 생태계 내에서 기준 통화 역할을 합니다.',
                'description_en': 'Stable value storage that serves as the base currency within the GLI ecosystem.',
                'features': [
                    '안정적인 가치 보장',
                    '법정화폐 페어링',
                    '크로스체인 호환',
                    '즉시 환전 가능',
                ],
                'total_supply': '무제한',
                'current_price': '$1.00',
                'order': 4,
                'is_active': True,
            },
        ]

        for token_data in tokens:
            token, created = TokenEcosystem.objects.get_or_create(
                symbol=token_data['symbol'],
                defaults=token_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✅ 생성됨: {token.symbol} - {token.name}'))
            else:
                self.stdout.write(f'  ⏭️  이미 존재: {token.symbol} - {token.name}')
