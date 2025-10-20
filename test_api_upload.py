#!/usr/bin/env python3
"""
실제 API 엔드포인트를 통한 이미지 업로드 테스트
"""
import os
import sys
import requests
import tempfile
from pathlib import Path
import time

# Django 설정
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth import authenticate
from apps.solana_auth.models import SolanaUser
from rest_framework_simplejwt.tokens import RefreshToken

BASE_URL = "http://127.0.0.1:8000"

def create_test_image():
    """테스트용 이미지 파일 생성"""
    # 임시 이미지 파일 생성
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')

    # 간단한 PNG 파일 바이너리 데이터 (1x1 픽셀 투명 PNG)
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x00\x01\x00\x00\x00\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

    temp_file.write(png_data)
    temp_file.close()

    print(f"✅ 테스트 이미지 생성: {temp_file.name}")
    return temp_file.name

def get_admin_token():
    """관리자 토큰 획득"""
    try:
        # Django에서 직접 토큰 생성 (슈퍼유저 계정 사용)
        admin_user = SolanaUser.objects.filter(is_superuser=True).first()

        if not admin_user:
            print("❌ 슈퍼유저를 찾을 수 없습니다.")
            return None

        refresh = RefreshToken.for_user(admin_user)
        access_token = str(refresh.access_token)

        print(f"✅ 토큰 생성 성공 (사용자: {admin_user.username})")
        return access_token

    except Exception as e:
        print(f"❌ 토큰 생성 실패: {e}")
        return None

def test_upload_api(token, image_path):
    """실제 업로드 API 테스트"""
    print(f"🔍 API 업로드 테스트 시작...")

    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        # 파일 업로드
        with open(image_path, 'rb') as f:
            files = {
                'file': ('test_image.png', f, 'image/png')
            }
            data = {
                'folder': 'test-api-upload'
            }

            print(f"📤 업로드 시작: {BASE_URL}/api/upload/image/")
            start_time = time.time()

            response = requests.post(
                f'{BASE_URL}/api/upload/image/',
                headers=headers,
                files=files,
                data=data,
                timeout=30  # 30초 타임아웃
            )

            end_time = time.time()
            upload_time = end_time - start_time

            print(f"⏱️  업로드 소요 시간: {upload_time:.2f}초")
            print(f"📊 응답 상태 코드: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"✅ 업로드 성공!")
                print(f"📄 응답 데이터:")
                print(f"   - URL: {result['data']['url']}")
                print(f"   - 파일명: {result['data']['filename']}")
                print(f"   - 크기: {result['data']['size']} bytes")
                print(f"   - Content-Type: {result['data']['content_type']}")
                return True, result
            else:
                print(f"❌ 업로드 실패: {response.status_code}")
                print(f"📄 오류 응답: {response.text}")
                return False, response.text

    except requests.Timeout:
        print(f"⏰ 업로드 타임아웃 (30초 초과)")
        return False, "Timeout"
    except Exception as e:
        print(f"❌ 업로드 중 오류: {e}")
        return False, str(e)

def test_team_member_creation_with_image(token, image_url):
    """이미지 URL을 사용한 팀 멤버 생성 테스트"""
    print(f"\n🔍 팀 멤버 생성 테스트 시작...")

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {
        'image_url': image_url,
        'position_ko': '테스트 직책',
        'position_en': 'Test Position',
        'role_ko': '테스트 역할',
        'role_en': 'Test Role',
        'tags': ['test', 'api'],
        'order': 999,
        'is_active': True
    }

    try:
        response = requests.post(
            f'{BASE_URL}/api/team-members/',
            headers=headers,
            json=data,
            timeout=10
        )

        print(f"📊 팀 멤버 생성 응답 상태 코드: {response.status_code}")

        if response.status_code == 201:
            result = response.json()
            print(f"✅ 팀 멤버 생성 성공!")
            print(f"📄 생성된 팀 멤버 ID: {result['id']}")
            print(f"📄 이미지 URL: {result['image_url']}")
            return True, result
        else:
            print(f"❌ 팀 멤버 생성 실패: {response.status_code}")
            print(f"📄 오류 응답: {response.text}")
            return False, response.text

    except Exception as e:
        print(f"❌ 팀 멤버 생성 중 오류: {e}")
        return False, str(e)

def cleanup_temp_file(file_path):
    """임시 파일 정리"""
    try:
        os.unlink(file_path)
        print(f"🗑️  임시 파일 삭제: {file_path}")
    except Exception as e:
        print(f"⚠️ 임시 파일 삭제 실패: {e}")

def main():
    print("=" * 60)
    print("GLI Platform API 업로드 테스트")
    print("=" * 60)

    # 1. 테스트 이미지 생성
    test_image_path = create_test_image()

    # 2. 관리자 토큰 획득
    token = get_admin_token()
    if not token:
        print("❌ 토큰을 획득할 수 없어 테스트를 중단합니다.")
        cleanup_temp_file(test_image_path)
        return False

    # 3. 이미지 업로드 테스트
    upload_success, upload_result = test_upload_api(token, test_image_path)

    if upload_success:
        # 4. 업로드된 이미지로 팀 멤버 생성 테스트
        image_url = upload_result['data']['url']
        member_success, member_result = test_team_member_creation_with_image(token, image_url)

        print("\n" + "=" * 60)
        print("테스트 결과 요약")
        print("=" * 60)
        print(f"이미지 업로드: {'✅ 성공' if upload_success else '❌ 실패'}")
        print(f"팀 멤버 생성: {'✅ 성공' if member_success else '❌ 실패'}")

        if upload_success and member_success:
            print("🎉 모든 API 테스트가 성공했습니다!")
            success = True
        else:
            print("❌ 일부 테스트가 실패했습니다.")
            success = False
    else:
        print("\n" + "=" * 60)
        print("테스트 결과 요약")
        print("=" * 60)
        print(f"이미지 업로드: ❌ 실패 - {upload_result}")
        print("❌ 업로드 실패로 인해 팀 멤버 생성 테스트를 건너뜁니다.")
        success = False

    # 5. 정리
    cleanup_temp_file(test_image_path)

    return success

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 테스트 실행 중 치명적인 오류: {e}")
        exit(1)