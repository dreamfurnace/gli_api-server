#!/usr/bin/env python
"""
전략 로드맵 페이즈 데이터 생성 스크립트
"""
import os
import sys
import django

# Django 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.solana_auth.models import StrategyPhase

def create_strategy_phases():
    """전략 로드맵 페이즈 데이터 생성"""

    # 기존 데이터 확인
    existing_count = StrategyPhase.objects.count()
    print(f"✅ 기존 전략 로드맵 페이즈 수: {existing_count}")

    # 전략 로드맵 페이즈 데이터
    phases_data = [
        {
            "icon": "🚀",
            "title_ko": "플랫폼 구축",
            "title_en": "Platform Development",
            "description_ko": "GLI 플랫폼의 기반을 구축하고 핵심 토큰을 발행합니다.",
            "description_en": "Build the foundation of the GLI platform and issue core tokens.",
            "features": ["웹 플랫폼 개발", "GLIB/GLID/GLIL 토큰 발행", "지갑 연동 시스템"],
            "order": 1,
            "is_active": True,
        },
        {
            "icon": "🏨",
            "title_ko": "리조트 연동",
            "title_en": "Resort Integration",
            "description_ko": "리조트 파트너십을 구축하고 예약 시스템을 연동합니다.",
            "description_en": "Establish resort partnerships and integrate the booking system.",
            "features": ["리조트 파트너십", "예약 시스템", "리워드 프로그램"],
            "order": 2,
            "is_active": True,
        },
        {
            "icon": "🎮",
            "title_ko": "게임 생태계",
            "title_en": "Gaming Ecosystem",
            "description_ko": "게임 콘텐츠와 NFT 컬렉션을 통해 메타버스 경험을 제공합니다.",
            "description_en": "Provide metaverse experiences through gaming content and NFT collections.",
            "features": ["게임 콘텐츠", "NFT 컬렉션", "메타버스 경험"],
            "order": 3,
            "is_active": True,
        },
        {
            "icon": "🌍",
            "title_ko": "글로벌 확장",
            "title_en": "Global Expansion",
            "description_ko": "글로벌 시장으로 진출하고 전략적 파트너십을 확대합니다.",
            "description_en": "Expand into global markets and grow strategic partnerships.",
            "features": ["글로벌 진출", "전략적 파트너십", "서비스 확장"],
            "order": 4,
            "is_active": True,
        },
    ]

    created_count = 0
    updated_count = 0

    for phase_data in phases_data:
        # 같은 제목이 이미 있는지 확인 (한글 기준)
        existing_phase = StrategyPhase.objects.filter(
            title_ko=phase_data["title_ko"]
        ).first()

        if existing_phase:
            # 기존 데이터 업데이트
            for key, value in phase_data.items():
                setattr(existing_phase, key, value)
            existing_phase.save()
            updated_count += 1
            print(f"📝 업데이트: {phase_data['icon']} {phase_data['title_ko']}")
        else:
            # 새로운 데이터 생성
            phase = StrategyPhase.objects.create(**phase_data)
            created_count += 1
            print(f"✨ 생성: {phase_data['icon']} {phase_data['title_ko']} (ID: {phase.id})")

    print(f"\n{'='*60}")
    print(f"✅ 작업 완료!")
    print(f"   - 새로 생성: {created_count}개")
    print(f"   - 업데이트: {updated_count}개")
    print(f"   - 총 페이즈: {StrategyPhase.objects.count()}개")
    print(f"{'='*60}\n")

    # 생성된 전략 로드맵 페이즈 목록 출력
    print("📋 현재 전략 로드맵 페이즈 목록:")
    for phase in StrategyPhase.objects.all().order_by('order'):
        status = "✅ 활성" if phase.is_active else "❌ 비활성"
        print(f"   {phase.order}. {phase.icon} {phase.title_ko} - {status}")
        print(f"      {phase.description_ko}")
        print(f"      주요 기능: {', '.join(phase.features)}")
        print(f"      ID: {phase.id}")
        print()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 GLI Platform 전략 로드맵 데이터 생성")
    print("="*60 + "\n")

    try:
        create_strategy_phases()
        print("✅ 스크립트 실행 완료!\n")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
