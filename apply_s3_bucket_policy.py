#!/usr/bin/env python
"""
S3 버킷에 public read 정책을 적용하는 스크립트
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
import requests
from django.conf import settings
from botocore.exceptions import ClientError

def apply_public_read_policy():
    """S3 버킷에 public read 정책 적용"""
    print("=== S3 버킷 Public Read 정책 적용 ===")

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION
    )

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    print(f"버킷명: {bucket_name}")

    # 적용할 정책
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

    print("\n적용할 정책:")
    print(json.dumps(bucket_policy, indent=2))

    try:
        # 정책 적용
        policy_json = json.dumps(bucket_policy)
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=policy_json
        )
        print("\n✅ 버킷 정책 적용 성공!")

        # 정책 적용 확인
        print("\n정책 적용 확인 중...")
        try:
            response = s3_client.get_bucket_policy(Bucket=bucket_name)
            applied_policy = json.loads(response['Policy'])
            print("✅ 정책이 성공적으로 적용되었습니다:")
            print(json.dumps(applied_policy, indent=2))
        except Exception as e:
            print(f"❌ 정책 확인 실패: {e}")

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'MalformedPolicy':
            print(f"❌ 정책 형식 오류: {e}")
        elif error_code == 'AccessDenied':
            print(f"❌ 접근 권한 없음: {e}")
            print("AWS 계정에 s3:PutBucketPolicy 권한이 필요합니다.")
        else:
            print(f"❌ 정책 적용 실패: {e}")
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")

def test_public_access():
    """정책 적용 후 public access 테스트"""
    print("\n=== Public Access 테스트 ===")

    # 기존 팀 멤버 이미지로 테스트
    try:
        from apps.solana_auth.models import TeamMember
        team_members = TeamMember.objects.filter(image_url__isnull=False)[:2]

        for member in team_members:
            if member.image_url and '.amazonaws.com' in member.image_url:
                print(f"\n팀 멤버: {member.position_ko}")

                # 원본 S3 URL 추출 (Presigned URL이 아닌 경우)
                original_url = member.image_url
                if '?' in original_url:
                    # Presigned URL에서 원본 URL 추출
                    original_url = original_url.split('?')[0]

                print(f"테스트 URL: {original_url}")

                # 직접 접근 테스트
                try:
                    response = requests.get(original_url, timeout=10)
                    if response.status_code == 200:
                        print("✅ 직접 접근 성공! 이미지를 영구적으로 접근할 수 있습니다.")
                    else:
                        print(f"❌ 직접 접근 실패: {response.status_code}")
                        if response.status_code == 403:
                            print("   정책이 아직 적용되지 않았을 수 있습니다. 몇 분 후 다시 시도해주세요.")
                except Exception as e:
                    print(f"❌ 접근 테스트 오류: {e}")

                # 첫 번째만 테스트하고 중단
                break

    except Exception as e:
        print(f"❌ 테스트 중 오류: {e}")

if __name__ == "__main__":
    print("S3 버킷 Public Read 정책 적용")
    print("="*50)

    apply_public_read_policy()
    test_public_access()

    print("\n" + "="*50)
    print("정책 적용 완료")
    print("\n⚠️  참고:")
    print("- 정책이 적용되기까지 몇 분이 걸릴 수 있습니다.")
    print("- 적용 후 모든 S3 파일이 누구나 접근 가능해집니다.")
    print("- Presigned URL 로직을 제거하고 직접 S3 URL을 사용할 수 있습니다.")