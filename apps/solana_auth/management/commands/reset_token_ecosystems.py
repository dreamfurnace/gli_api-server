from django.core.management.base import BaseCommand
from apps.solana_auth.models import TokenEcosystem


class Command(BaseCommand):
    help = '토큰 에코시스템 데이터 초기화 및 재설정'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🔄 토큰 에코시스템 데이터를 초기화합니다...'))

        # 기존 데이터 삭제
        deleted_count = TokenEcosystem.objects.all().count()
        TokenEcosystem.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ 기존 데이터 {deleted_count}개 삭제 완료'))

        # 새로운 토큰 데이터
        tokens = [
            {
                'icon': '🔵',
                'name': 'GLI Business',
                'symbol': 'GLIB',
                'description_ko': 'GLIB는 실물자산 기반의 투자형 코인으로, 동남아 부동산 및 사업 아이템에 투자됩니다.\n수익률에 따른 배당이 제공되며, 거래소 상장 계획은 없고, 일정 등급 이상의 보유자에게 주식매수권이 부여됩니다.',
                'description_en': 'GLIB is a real-asset investment token for Southeast Asian real estate and business ventures.\nHolders receive dividends based on performance; no exchange listing is planned. High-tier holders may be granted stock purchase rights.',
                'features_ko': [
                    '프리세일을 통해 구매',
                    '수익률에 따른 배당',
                    '거래소 상장 계획 없음',
                    '등급 및 보유량에 따라 혜택 차등',
                    '주식매수권 부여',
                ],
                'features_en': [
                    'Purchase via presale',
                    'Dividend distribution by yield',
                    'No exchange listing plan',
                    'Tiered benefits by holding volume',
                    'Stock purchase rights granted',
                ],
                'total_supply': '1,000,000,000',
                'current_price': '$1',
                'order': 1,
                'is_active': True,
            },
            {
                'icon': '🔷',
                'name': 'GLI Governance',
                'symbol': 'GLID',
                'description_ko': 'GLID는 플랫폼의 의사결정과 운영 투표에 참여할 수 있는 거버넌스 코인입니다.\n투자 사업 아이템 및 중개 서비스 수수료 지불에 활용되며, 거래소 상장 가능한 주요 유통 토큰입니다.',
                'description_en': 'GLID is a governance token enabling participation in platform voting and decision-making.\nUsed for investment project voting and service fee payments. It serves as a tradable exchange-listed governance asset.',
                'features_ko': [
                    '투자 사업 아이템 투표 참여',
                    '중개 서비스 수수료 지불',
                    '투자 포트폴리오 검토',
                    '사업 일정 및 순위 검토',
                    '거래소 상장 토큰',
                ],
                'features_en': [
                    'Participate in investment project voting',
                    'Pay brokerage and service fees',
                    'Review investment portfolios',
                    'Evaluate business schedules and priorities',
                    'Exchange-listed governance token',
                ],
                'total_supply': '500,000,000',
                'current_price': '$0.8',
                'order': 2,
                'is_active': True,
            },
            {
                'icon': '🔹',
                'name': 'GLI Leisure',
                'symbol': 'GLIL',
                'description_ko': 'GLIL은 오프체인에서 사용되는 게임 및 레저 포인트로, 동남아 레저 상품 이용에 사용됩니다.\n현금 전환이 불가하며, 미화 달러에 1:1 페깅되어 GLI 플랫폼 내에서만 교환 가능합니다.',
                'description_en': 'GLIL is an off-chain game and leisure point used for Southeast Asian leisure services.\nIt is non-convertible to cash, pegged 1:1 with USD, and exchangeable only within the GLI platform.',
                'features_ko': [
                    '게임 생태계 전용 포인트',
                    '현금 환전 불가',
                    '미화 달러 1:1 페깅',
                    '상장 및 세일 계획 없음',
                    'GLI 플랫폼 내 교환 가능',
                ],
                'features_en': [
                    'Used within the gaming ecosystem',
                    'Not convertible to cash',
                    'Pegged 1:1 to USD',
                    'No listing or sale plan',
                    'Exchangeable within GLI platform',
                ],
                'total_supply': '2,000,000,000',
                'current_price': '$1',
                'order': 3,
                'is_active': True,
            },
        ]

        # 새로운 데이터 삽입
        self.stdout.write('🌱 새로운 토큰 에코시스템 데이터를 생성합니다...')
        created_count = 0
        for token_data in tokens:
            token = TokenEcosystem.objects.create(**token_data)
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'  ✅ 생성됨: {token.symbol} - {token.name}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ 토큰 에코시스템 데이터 초기화 완료! (총 {created_count}개 생성)'))
