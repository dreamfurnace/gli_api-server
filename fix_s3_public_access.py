#!/usr/bin/env python
"""
S3 버킷 public access 설정 직접 해결 스크립트
"""
import os
import sys
import django
from pathlib import Path

# Django 설정 초기화
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import boto3
import json
from django.conf import settings
from botocore.exceptions import ClientError

def fix_s3_public_access():
    """S3 버킷 public access 문제 해결"""
    print("=== S3 Public Access 문제 해결 ===")

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION
    )

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    print(f"버킷명: {bucket_name}")

    # 1단계: Public Access Block 해제 시도
    print("\n1️⃣ Public Access Block 해제 시도...")
    try:
        s3_client.delete_public_access_block(Bucket=bucket_name)
        print("✅ Public Access Block 해제 성공")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDenied':
            print("❌ Public Access Block 해제 권한 없음")
            print("   → AWS 콘솔에서 수동 해제 필요")
        else:
            print(f"❌ Public Access Block 해제 실패: {e}")

    # 2단계: 버킷 정책 설정 시도
    print("\n2️⃣ 버킷 정책 설정 시도...")
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }

    try:
        policy_json = json.dumps(bucket_policy)
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=policy_json
        )
        print("✅ 버킷 정책 설정 성공")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDenied':
            print("❌ 버킷 정책 설정 권한 없음")
        elif 'BlockPublicPolicy' in str(e):
            print("❌ Public Access Block에 의해 차단됨")
            print("   → 먼저 AWS 콘솔에서 Block Public Access 해제 필요")
        else:
            print(f"❌ 버킷 정책 설정 실패: {e}")

    # 3단계: 테스트 파일 업로드 및 접근 테스트
    print("\n3️⃣ 직접 URL 접근 테스트...")
    test_url_direct_access()

def test_url_direct_access():
    """기존 팀 멤버 이미지 직접 접근 테스트"""
    try:
        from apps.solana_auth.models import TeamMember
        import requests

        team_members = TeamMember.objects.filter(image_url__isnull=False)[:2]

        for member in team_members:
            if member.image_url:
                # 원본 S3 URL 추출 (쿼리 파라미터 제거)
                original_url = member.image_url.split('?')[0] if '?' in member.image_url else member.image_url

                print(f"\n팀 멤버: {member.position_ko}")
                print(f"테스트 URL: {original_url}")

                try:
                    response = requests.get(original_url, timeout=5)
                    if response.status_code == 200:
                        print("✅ 직접 접근 성공!")
                    elif response.status_code == 403:
                        print("❌ 403 Forbidden - Public Access 차단됨")
                    else:
                        print(f"❌ 접근 실패: HTTP {response.status_code}")
                except Exception as e:
                    print(f"❌ 접근 테스트 오류: {e}")

    except Exception as e:
        print(f"❌ 테스트 중 오류: {e}")

def show_manual_solution():
    """수동 해결 방법 안내"""
    print("\n" + "="*60)
    print("🛠️  수동 해결 방법 (AWS 콘솔)")
    print("="*60)
    print("\n현재 GLI 사용자는 S3 관리 권한이 제한적입니다.")
    print("AWS 루트 계정 또는 관리자 권한으로 다음 설정을 진행해주세요:")

    print("\n📋 **1. AWS S3 콘솔 접속**")
    print("   https://s3.console.aws.amazon.com/")

    print("\n📋 **2. gli-platform-media-staging 버킷 선택**")

    print("\n📋 **3. Permissions 탭 → Block public access 설정**")
    print("   - 'Edit' 클릭")
    print("   - 'Block all public policies' 체크 해제")
    print("   - 'Save changes' 클릭")

    print("\n📋 **4. Bucket policy 설정**")
    print("   - 'Bucket policy' 섹션에서 'Edit' 클릭")
    print("   - 다음 정책 입력:")
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::gli-platform-media-staging/*"
            }
        ]
    }
    print(json.dumps(policy, indent=2))

    print("\n✅ **설정 완료 후:**")
    print("   - 모든 이미지가 영구적으로 접근 가능해집니다")
    print("   - Presigned URL 없이 직접 S3 URL 사용 가능")
    print("   - 웹사이트 성능 향상")

if __name__ == "__main__":
    print("GLI Platform S3 Public Access 문제 해결")
    print("="*50)

    fix_s3_public_access()
    show_manual_solution()

    print("\n" + "="*50)
    print("스크립트 완료")