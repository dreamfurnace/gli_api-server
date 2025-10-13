#!/usr/bin/env python
"""
프로젝트 특징 데이터 생성 스크립트
"""
import os
import sys
import django

# Django 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.solana_auth.models import ProjectFeature

def create_project_features():
    """프로젝트 특징 데이터 생성"""

    # 기존 데이터 확인
    existing_count = ProjectFeature.objects.count()
    print(f"✅ 기존 프로젝트 특징 수: {existing_count}")

    # 프로젝트 특징 데이터
    features_data = [
        {
            "icon": "🌊",
            "title_ko": "비전",
            "title_en": "Vision",
            "description_ko": "GLI는 리조트 경험과 블록체인 기술을 융합하여 새로운 가치를 창출합니다.",
            "description_en": "GLI creates new value by merging resort experiences with blockchain technology.",
            "order": 1,
            "is_active": True,
        },
        {
            "icon": "🔗",
            "title_ko": "블록체인 혁신",
            "title_en": "Blockchain Innovation",
            "description_ko": "RWA 토큰을 통해 실물 자산과 디지털 자산을 연결하는 혁신적인 생태계를 구축합니다.",
            "description_en": "We build an innovative ecosystem connecting physical assets and digital assets through RWA tokens.",
            "order": 2,
            "is_active": True,
        },
        {
            "icon": "🏖️",
            "title_ko": "프리미엄 리조트",
            "title_en": "Premium Resort",
            "description_ko": "최고급 리조트 서비스와 독점적인 경험을 토큰 홀더에게 제공합니다.",
            "description_en": "We provide premium resort services and exclusive experiences to token holders.",
            "order": 3,
            "is_active": True,
        },
        {
            "icon": "🎮",
            "title_ko": "게임 생태계",
            "title_en": "Gaming Ecosystem",
            "description_ko": "재미있는 게임 요소를 통해 사용자 참여를 높이고 토큰 유틸리티를 확장합니다.",
            "description_en": "We increase user engagement and expand token utility through fun gaming elements.",
            "order": 4,
            "is_active": True,
        },
    ]

    created_count = 0
    updated_count = 0

    for feature_data in features_data:
        # 같은 제목이 이미 있는지 확인 (한글 기준)
        existing_feature = ProjectFeature.objects.filter(
            title_ko=feature_data["title_ko"]
        ).first()

        if existing_feature:
            # 기존 데이터 업데이트
            for key, value in feature_data.items():
                setattr(existing_feature, key, value)
            existing_feature.save()
            updated_count += 1
            print(f"📝 업데이트: {feature_data['icon']} {feature_data['title_ko']}")
        else:
            # 새로운 데이터 생성
            feature = ProjectFeature.objects.create(**feature_data)
            created_count += 1
            print(f"✨ 생성: {feature_data['icon']} {feature_data['title_ko']} (ID: {feature.id})")

    print(f"\n{'='*60}")
    print(f"✅ 작업 완료!")
    print(f"   - 새로 생성: {created_count}개")
    print(f"   - 업데이트: {updated_count}개")
    print(f"   - 총 특징: {ProjectFeature.objects.count()}개")
    print(f"{'='*60}\n")

    # 생성된 프로젝트 특징 목록 출력
    print("📋 현재 프로젝트 특징 목록:")
    for feature in ProjectFeature.objects.all().order_by('order'):
        status = "✅ 활성" if feature.is_active else "❌ 비활성"
        print(f"   {feature.order}. {feature.icon} {feature.title_ko} - {status}")
        print(f"      {feature.description_ko}")
        print(f"      ID: {feature.id}")
        print()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 GLI Platform 프로젝트 특징 데이터 생성")
    print("="*60 + "\n")

    try:
        create_project_features()
        print("✅ 스크립트 실행 완료!\n")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
