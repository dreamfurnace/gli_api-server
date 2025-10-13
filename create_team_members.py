#!/usr/bin/env python
"""
팀 구성원 데이터 생성 스크립트
"""
import os
import sys
import django

# Django 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.solana_auth.models import TeamMember

def create_team_members():
    """팀 구성원 데이터 생성"""

    # 기존 데이터 확인
    existing_count = TeamMember.objects.count()
    print(f"✅ 기존 팀 구성원 수: {existing_count}")

    # 팀 구성원 데이터
    team_members_data = [
        {
            "image_url": "",  # 추후 어드민에서 업로드 가능
            "position_ko": "최고운영책임자(COO)",
            "position_en": "Chief Operating Officer (COO)",
            "role_ko": "AI 및 블록체인 MBA. Dcoin.com 전 COO, 글로벌 론칭을 이끌고 CMC 기준 12위 달성. 600개 이상의 백서 검토.",
            "role_en": "MBA in AI and Blockchain. Former COO at Dcoin.com, led global launch and achieved rank 12 on CMC. Reviewed over 600 whitepapers.",
            "tags": ["expert", "BM"],
            "order": 1,
            "is_active": True,
        },
        {
            "image_url": "",  # 추후 어드민에서 업로드 가능
            "position_ko": "최고기술책임자(CTO)",
            "position_en": "Chief Technology Officer (CTO)",
            "role_ko": "서울대학교 졸업. BTCC Korea 전 개발 이사, 40명 규모의 기술팀 구축. 거래소 및 월렛 아키텍처 전문가.",
            "role_en": "Seoul National University graduate. Former Development Director at BTCC Korea, built a tech team of 40. Expert in exchange and wallet architecture.",
            "tags": ["tech", "AI", "contract", "platform"],
            "order": 2,
            "is_active": True,
        },
        {
            "image_url": "",  # 추후 어드민에서 업로드 가능
            "position_ko": "최고컴플라이언스책임자(CCO)",
            "position_en": "Chief Compliance Officer (CCO)",
            "role_ko": "서울대학교 졸업. 거래소 상장 심사 및 사업 개발 주도. 탈중앙화 거래소(DEX) 프로젝트 및 규제 준수 담당.",
            "role_en": "Seoul National University graduate. Led exchange listing review and business development. Responsible for DEX projects and regulatory compliance.",
            "tags": ["cert", "IR"],
            "order": 3,
            "is_active": True,
        },
    ]

    created_count = 0
    updated_count = 0

    for member_data in team_members_data:
        # 같은 직책이 이미 있는지 확인
        existing_member = TeamMember.objects.filter(
            position_ko=member_data["position_ko"]
        ).first()

        if existing_member:
            # 기존 데이터 업데이트
            for key, value in member_data.items():
                setattr(existing_member, key, value)
            existing_member.save()
            updated_count += 1
            print(f"📝 업데이트: {member_data['position_ko']}")
        else:
            # 새로운 데이터 생성
            member = TeamMember.objects.create(**member_data)
            created_count += 1
            print(f"✨ 생성: {member_data['position_ko']} (ID: {member.id})")

    print(f"\n{'='*60}")
    print(f"✅ 작업 완료!")
    print(f"   - 새로 생성: {created_count}명")
    print(f"   - 업데이트: {updated_count}명")
    print(f"   - 총 팀원: {TeamMember.objects.count()}명")
    print(f"{'='*60}\n")

    # 생성된 팀 구성원 목록 출력
    print("📋 현재 팀 구성원 목록:")
    for member in TeamMember.objects.all().order_by('order'):
        status = "✅ 활성" if member.is_active else "❌ 비활성"
        print(f"   {member.order}. {member.position_ko} - {status}")
        print(f"      태그: {', '.join(member.tags)}")
        print(f"      ID: {member.id}")
        print()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 GLI Platform 팀 구성원 데이터 생성")
    print("="*60 + "\n")

    try:
        create_team_members()
        print("✅ 스크립트 실행 완료!\n")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
