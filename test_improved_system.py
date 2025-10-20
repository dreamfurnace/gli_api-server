#!/usr/bin/env python
"""
개선된 7일 유효기간 Presigned URL 시스템 테스트
"""
import os
import sys
import django
from pathlib import Path

# Django 설정 초기화
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import requests
from datetime import datetime, timedelta
from apps.solana_auth.models import TeamMember
from apps.solana_auth.serializers import TeamMemberSerializer

def test_improved_system():
    """개선된 7일 유효기간 시스템 테스트"""
    print("=== 개선된 Presigned URL 시스템 테스트 ===")
    print(f"테스트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # 기존 팀 멤버들의 이미지 URL 확인
        team_members = TeamMember.objects.filter(image_url__isnull=False)[:3]

        if not team_members:
            print("❌ 테스트할 팀 멤버 데이터가 없습니다.")
            return

        print(f"\n📊 총 {len(team_members)}개 팀 멤버 이미지 테스트:")

        success_count = 0
        for i, member in enumerate(team_members, 1):
            print(f"\n{i}. 팀 멤버: {member.position_ko}")

            # Serializer를 통해 Presigned URL 생성
            serializer = TeamMemberSerializer(member)
            serialized_data = serializer.data

            image_url = serialized_data.get('image_url')
            if image_url:
                print(f"   이미지 URL: {image_url}")

                # URL 유효성 검사
                if '?X-Amz-Expires=' in image_url:
                    # 만료 시간 추출
                    try:
                        expires_part = image_url.split('X-Amz-Expires=')[1].split('&')[0]
                        expires_seconds = int(expires_part)
                        expires_days = expires_seconds / 86400  # 초를 일로 변환

                        print(f"   ✅ Presigned URL 유효기간: {expires_days:.1f}일")

                        if abs(expires_days - 7) < 0.1:  # 7일에 가까우면 성공
                            print(f"   ✅ 7일 유효기간 설정 확인!")
                            success_count += 1
                        else:
                            print(f"   ❌ 예상과 다른 유효기간: {expires_days:.1f}일 (예상: 7일)")

                    except Exception as e:
                        print(f"   ❌ 만료 시간 파싱 오류: {e}")
                else:
                    print(f"   ❌ Presigned URL 형식이 아님")

                # URL 접근 테스트
                try:
                    response = requests.get(image_url, timeout=5)
                    if response.status_code == 200:
                        print(f"   ✅ 이미지 접근 성공 ({response.status_code})")
                    else:
                        print(f"   ❌ 이미지 접근 실패 ({response.status_code})")
                except Exception as e:
                    print(f"   ❌ 접근 테스트 오류: {e}")
            else:
                print(f"   ❌ 이미지 URL이 없음")

        print(f"\n📈 결과 요약:")
        print(f"   - 총 테스트: {len(team_members)}개")
        print(f"   - 7일 유효기간 설정 성공: {success_count}개")
        print(f"   - 성공률: {(success_count/len(team_members)*100):.1f}%")

        if success_count == len(team_members):
            print("\n🎉 모든 이미지가 7일 유효기간 Presigned URL로 정상 작동중!")
        else:
            print(f"\n⚠️  일부 이미지에 문제가 있습니다.")

    except Exception as e:
        print(f"❌ 테스트 중 오류: {e}")

def show_aws_instructions():
    """AWS 설정 방법 안내"""
    print("\n" + "="*60)
    print("🔧 AWS S3 영구적 Public Access 설정 방법")
    print("="*60)

    print("\n📋 **AWS 콘솔에서 Block Public Access 해제:**")
    print("1. AWS S3 콘솔 접속: https://s3.console.aws.amazon.com/")
    print("2. `gli-platform-media-staging` 버킷 선택")
    print("3. **'Permissions' 탭** 클릭")
    print("4. **'Block public access'** 섹션에서 **'Edit'** 클릭")
    print("5. **'Block all public policies'** 체크박스 **해제** ✅")
    print("6. **'Save changes'** 후 확인")

    print("\n📋 **S3 Bucket Policy 설정:**")
    print("7. 같은 Permissions 탭에서 **'Bucket policy'** 섹션 찾기")
    print("8. **'Edit'** 클릭 후 다음 정책 입력:")
    print("""
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::gli-platform-media-staging/*"
    }
  ]
}""")
    print("9. **'Save changes'** 클릭")

    print("\n📋 **설정 후 테스트:**")
    print("10. 몇 분 후 `python apply_s3_bucket_policy.py` 재실행")
    print("11. 정책 적용 확인 및 public access 테스트")

    print("\n⚠️  **주의사항:**")
    print("- 설정 후 모든 S3 파일이 누구나 접근 가능해집니다")
    print("- 보안이 중요한 파일은 다른 버킷 사용 권장")
    print("- 정책 적용까지 최대 5분 소요될 수 있습니다")

    print("\n✅ **설정 완료 후 장점:**")
    print("- 이미지 URL이 영구적으로 접근 가능")
    print("- Presigned URL 생성 오버헤드 없음")
    print("- 더 빠른 이미지 로딩 속도")

def show_current_solution():
    """현재 7일 유효기간 솔루션 설명"""
    print("\n" + "="*60)
    print("🔄 현재 적용된 7일 유효기간 솔루션")
    print("="*60)

    print("\n✅ **개선된 점:**")
    print("- 기존 24시간 → 7일 유효기간으로 연장")
    print("- 새 업로드와 기존 이미지 모두 7일 접근 가능")
    print("- 일주일 동안은 끊김없이 이미지 표시")

    print("\n📅 **7일 후 갱신 방법:**")
    print("- 관리자 페이지에서 팀 멤버 정보 조회 시 자동 갱신")
    print("- API 호출 시마다 새로운 7일 유효기간 Presigned URL 생성")
    print("- 사용자가 페이지를 방문할 때마다 URL이 갱신됨")

    print("\n🔄 **자동 갱신 로직:**")
    print("- 팀 멤버 목록 API 호출 → 자동으로 새 Presigned URL 생성")
    print("- 기존 URL이 만료되기 전에 새 URL로 자동 교체")
    print("- 사용자는 만료를 경험하지 않음")

if __name__ == "__main__":
    print("GLI Platform - 개선된 이미지 접근 시스템 테스트")
    print("="*60)

    test_improved_system()
    show_current_solution()
    show_aws_instructions()

    print("\n" + "="*60)
    print("테스트 완료! 🎯")