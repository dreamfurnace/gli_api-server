"""
개발 일정 데이터를 데이터베이스에 삽입하는 Django management command
실행: python manage.py load_development_timeline
"""
from django.core.management.base import BaseCommand
from apps.solana_auth.models import DevelopmentTimeline


class Command(BaseCommand):
    help = 'GLI 개발 일정 10개 데이터를 데이터베이스에 삽입합니다'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='기존 데이터를 삭제하고 새로 추가합니다',
        )

    def handle(self, *args, **options):
        # 기존 데이터 삭제 옵션
        if options['clear']:
            deleted_count = DevelopmentTimeline.objects.all().count()
            DevelopmentTimeline.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'기존 개발 일정 데이터 {deleted_count}개를 삭제했습니다.')
            )

        # 10개의 개발 일정 데이터
        timeline_data = [
            {
                'quarter': '2025 Q2',
                'status_icon': '🟩',
                'title_ko': 'IR 및 법인 설립 준비',
                'title_en': 'IR & Entity Setup',
                'description_ko': 'IR 자료 및 홍보 콘텐츠 제작을 완료하고, 법인 설립 및 해외 ESTA 관련 초기 행정 절차를 진행합니다.',
                'description_en': 'Complete IR and marketing materials, and initiate corporate setup and overseas administrative (ESTA) procedures.',
                'order': 1,
                'is_active': True,
            },
            {
                'quarter': '2025 Q3',
                'status_icon': '🟩',
                'title_ko': '글로벌 여행 및 레저 상품 기획',
                'title_en': 'Global Travel & Leisure Product Planning',
                'description_ko': '해외 파트너사와 협력하여 여행·레저 상품을 공동 기획하고 현지 제휴 체계를 마련합니다.',
                'description_en': 'Collaborate with global partners to co-develop travel and leisure products and establish local alliances.',
                'order': 2,
                'is_active': True,
            },
            {
                'quarter': '2025 Q4',
                'status_icon': '⏳',
                'title_ko': '웹 플랫폼 개발 착수',
                'title_en': 'Web Platform Development Start',
                'description_ko': 'GLI 생태계의 핵심인 웹 플랫폼 개발을 시작하고, UX·UI 및 백엔드 구조 설계를 완료합니다.',
                'description_en': 'Begin core web platform development for the GLI ecosystem, completing UX/UI and backend architecture design.',
                'order': 3,
                'is_active': True,
            },
            {
                'quarter': '2026 Q1',
                'status_icon': '🕐',
                'title_ko': '해외 실물자산(RWA) 프로젝트 개발',
                'title_en': 'Overseas RWA Project Development',
                'description_ko': '해외 리조트·호텔 등 실물자산 기반 프로젝트를 발굴하고, RWA 토큰 발행 구조를 설계합니다.',
                'description_en': 'Identify overseas asset-backed projects such as resorts and hotels, and design the RWA token issuance model.',
                'order': 4,
                'is_active': True,
            },
            {
                'quarter': '2026 Q2',
                'status_icon': '⏳',
                'title_ko': 'GLI 플랫폼 핵심 토큰 발행',
                'title_en': 'GLI Core Token Issuance',
                'description_ko': 'GLIB / GLID / GLIL 토큰을 발행하고, 온체인 기반의 지갑 연동 시스템을 구축합니다.',
                'description_en': 'Issue GLIB / GLID / GLIL tokens and deploy on-chain wallet integration systems.',
                'order': 5,
                'is_active': True,
            },
            {
                'quarter': '2026 Q3',
                'status_icon': '🟩',
                'title_ko': '멤버십 여행 플랫폼 출시',
                'title_en': 'Launch of Membership Travel Platform',
                'description_ko': '멤버십 기반 여행 및 레저 상품을 정식 출시하며, 글로벌 이용자를 대상으로 커뮤니티를 확장합니다.',
                'description_en': 'Launch the membership-based travel and leisure platform, expanding community engagement worldwide.',
                'order': 6,
                'is_active': True,
            },
            {
                'quarter': '2026 Q4',
                'status_icon': '🕐',
                'title_ko': 'SERIES A 펀딩',
                'title_en': 'Series A Funding',
                'description_ko': '60억 원 규모의 시드 펀딩에 이어, 플랫폼 고도화 및 글로벌 확장을 위한 Series A 라운드를 진행합니다.',
                'description_en': 'Following the 6B KRW seed funding, initiate Series A round for platform expansion and global scaling.',
                'order': 7,
                'is_active': True,
            },
            {
                'quarter': '2027 Q2',
                'status_icon': '⏳',
                'title_ko': '디지털자산 거래소 개발',
                'title_en': 'Digital Asset Exchange Development',
                'description_ko': 'STO 및 가상자산이 통합된 라이선스 기반 거래소를 구축하고, DeFi 생태계 확장을 위한 연동 시스템을 개발합니다.',
                'description_en': 'Develop a licensed exchange integrating STO and crypto markets, with DeFi ecosystem interoperability.',
                'order': 8,
                'is_active': True,
            },
            {
                'quarter': '2028 Q1',
                'status_icon': '🟩',
                'title_ko': '거래소 정식 오픈',
                'title_en': 'Exchange Official Launch',
                'description_ko': '디지털자산 거래소를 정식 오픈하여, GLI 생태계 내 자산 순환 구조를 완성합니다.',
                'description_en': "Officially launch the digital asset exchange, completing GLI's internal asset circulation ecosystem.",
                'order': 9,
                'is_active': True,
            },
            {
                'quarter': '2029 Q2',
                'status_icon': '🚀',
                'title_ko': 'IPO (나스닥 상장 추진)',
                'title_en': 'IPO (NASDAQ Listing Initiative)',
                'description_ko': '글로벌 소셜 게이밍 및 투자 생태계를 기반으로 북미 중심의 IPO를 추진합니다.',
                'description_en': 'Pursue IPO on NASDAQ, leveraging global social gaming and investment ecosystem.',
                'order': 10,
                'is_active': True,
            },
        ]

        # 데이터 삽입
        created_count = 0
        updated_count = 0

        for data in timeline_data:
            # 같은 quarter를 가진 항목이 있는지 확인
            existing = DevelopmentTimeline.objects.filter(quarter=data['quarter']).first()

            if existing:
                # 기존 항목 업데이트
                for key, value in data.items():
                    setattr(existing, key, value)
                existing.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ [{data["quarter"]}] {data["title_ko"]} (업데이트)')
                )
            else:
                # 새 항목 생성
                DevelopmentTimeline.objects.create(**data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✨ [{data["quarter"]}] {data["title_ko"]} (신규 생성)')
                )

        # 결과 출력
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'개발 일정 데이터 삽입 완료!'))
        self.stdout.write(self.style.SUCCESS(f'신규 생성: {created_count}개'))
        self.stdout.write(self.style.SUCCESS(f'업데이트: {updated_count}개'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
