"""
전략 로드맵 데이터를 데이터베이스에 삽입하는 Django management command
실행: python manage.py load_strategy_roadmap
"""
from django.core.management.base import BaseCommand
from apps.solana_auth.models import StrategyPhase


class Command(BaseCommand):
    help = 'GLI 전략 로드맵 5단계 데이터를 데이터베이스에 삽입합니다'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='기존 데이터를 삭제하고 새로 추가합니다',
        )

    def handle(self, *args, **options):
        # 기존 데이터 삭제 옵션
        if options['clear']:
            deleted_count = StrategyPhase.objects.all().count()
            StrategyPhase.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'기존 전략 로드맵 데이터 {deleted_count}개를 삭제했습니다.')
            )

        # 5단계 전략 로드맵 데이터
        roadmap_data = [
            {
                'icon': '🪙',
                'title_ko': '실물자산 토큰화 (RWA)',
                'title_en': 'Real-World Asset Tokenization',
                'description_ko': '실물자산 토큰(RWA) 운용을 통해 안정적인 수익 기반을 확보하고 초기 투자 생태계를 형성합니다.',
                'description_en': 'Secure stable returns through real-world asset (RWA) token operations and establish the initial investment ecosystem.',
                'features_ko': [
                    '부동산·리조트 RWA 토큰 발행',
                    '실물 담보 기반 운용 모델',
                    '안정형 투자 상품 출시',
                ],
                'features_en': [
                    'Real estate and resort RWA token issuance',
                    'Asset-backed operation model',
                    'Launch of stable investment products',
                ],
                'order': 0,
                'is_active': True,
            },
            {
                'icon': '🌐',
                'title_ko': '글로벌 커뮤니티 확장',
                'title_en': 'Global Community Expansion',
                'description_ko': '글로벌 여행·레저 플랫폼 기반의 토큰 커뮤니티를 구축하고, 브랜드 마케팅 파워를 강화합니다.',
                'description_en': 'Build a token-based global community around travel and leisure platforms and enhance brand marketing power.',
                'features_ko': [
                    '글로벌 레저 파트너십 구축',
                    '커뮤니티 리워드 프로그램',
                    '마케팅 DAO 운영',
                ],
                'features_en': [
                    'Global leisure partnerships',
                    'Community reward programs',
                    'Marketing DAO operations',
                ],
                'order': 1,
                'is_active': True,
            },
            {
                'icon': '💱',
                'title_ko': '라이선스 기반 디지털 자산 거래소 설립',
                'title_en': 'Licensed Digital Asset Exchange',
                'description_ko': 'GLI 생태계를 연결하는 허브로서, STO와 가상자산을 아우르는 거래소를 설립하여 DeFi 인프라를 확장합니다.',
                'description_en': "Establish a licensed exchange connecting GLI's ecosystem, integrating STO and crypto markets to expand DeFi infrastructure.",
                'features_ko': [
                    'STO 및 가상자산 상장',
                    '규제 대응형 거래 시스템',
                    '온·오프체인 연동 결제 시스템',
                ],
                'features_en': [
                    'STO and crypto listings',
                    'Regulatory-compliant trading system',
                    'On-chain/off-chain payment integration',
                ],
                'order': 2,
                'is_active': True,
            },
            {
                'icon': '🎰',
                'title_ko': '소셜 카지노 플랫폼 확장',
                'title_en': 'Social Casino Platform Expansion',
                'description_ko': '소셜 카지노와 레저 플랫폼의 결합을 통해 수익성과 이용자 참여를 극대화하고, 매출 1천억 원 달성을 목표로 합니다.',
                'description_en': 'Combine social casino and leisure platforms to maximize profitability and user engagement, targeting KRW 100 billion in revenue.',
                'features_ko': [
                    '카지노 게임·NFT 연동',
                    '크로스체인 결제 시스템',
                    '유저 랭킹 및 리워드 구조',
                ],
                'features_en': [
                    'Casino games integrated with NFTs',
                    'Cross-chain payment system',
                    'User ranking and reward mechanisms',
                ],
                'order': 3,
                'is_active': True,
            },
            {
                'icon': '🚀',
                'title_ko': '글로벌 상장 및 지속 성장',
                'title_en': 'Global Listing and Sustainable Growth',
                'description_ko': '소셜 카지노 게임사로서 지속적인 성장 기반을 마련하고, 북미 시장 중심으로 나스닥 상장을 추진합니다.',
                'description_en': 'Build a foundation for sustainable growth as a social gaming company and pursue NASDAQ listing in North America.',
                'features_ko': [
                    '북미 시장 진출',
                    '글로벌 상장 준비 및 IR 강화',
                    '지속 가능한 Web3 비즈니스 모델 확립',
                ],
                'features_en': [
                    'Expansion into North American markets',
                    'IPO readiness and investor relations',
                    'Establish sustainable Web3 business model',
                ],
                'order': 4,
                'is_active': True,
            },
        ]

        # 데이터 삽입
        created_count = 0
        updated_count = 0

        for data in roadmap_data:
            # 같은 order를 가진 항목이 있는지 확인
            existing = StrategyPhase.objects.filter(order=data['order']).first()

            if existing:
                # 기존 항목 업데이트
                for key, value in data.items():
                    setattr(existing, key, value)
                existing.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ [{data["order"] + 1}] {data["title_ko"]} (업데이트)')
                )
            else:
                # 새 항목 생성
                StrategyPhase.objects.create(**data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✨ [{data["order"] + 1}] {data["title_ko"]} (신규 생성)')
                )

        # 결과 출력
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'전략 로드맵 데이터 삽입 완료!'))
        self.stdout.write(self.style.SUCCESS(f'신규 생성: {created_count}개'))
        self.stdout.write(self.style.SUCCESS(f'업데이트: {updated_count}개'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
