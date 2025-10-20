#!/usr/bin/env python
"""
S3 버킷의 public access 정책을 확인하고 테스트하는 스크립트
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
import requests
from django.conf import settings
from apps.solana_auth.utils.s3_upload import S3Uploader
from botocore.exceptions import ClientError

def test_s3_bucket_policy():
    """S3 버킷 정책 확인"""
    print("=== S3 버킷 정책 확인 ===")

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION
    )

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    print(f"버킷명: {bucket_name}")

    # 버킷 정책 확인
    try:
        policy_result = s3_client.get_bucket_policy(Bucket=bucket_name)
        print("현재 버킷 정책:")
        print(policy_result['Policy'])
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucketPolicy':
            print("❌ 버킷에 정책이 설정되지 않음")
        else:
            print(f"❌ 버킷 정책 확인 실패: {e}")

    # 버킷 ACL 확인
    try:
        acl_result = s3_client.get_bucket_acl(Bucket=bucket_name)
        print("\n현재 버킷 ACL:")
        for grant in acl_result['Grants']:
            grantee = grant.get('Grantee', {})
            permission = grant.get('Permission')
            if grantee.get('Type') == 'Group':
                print(f"  - {grantee.get('URI', 'Unknown')}: {permission}")
            else:
                print(f"  - {grantee.get('DisplayName', 'Owner')}: {permission}")
    except ClientError as e:
        print(f"❌ 버킷 ACL 확인 실패: {e}")

def test_public_read_acl():
    """Public-read ACL 설정 테스트"""
    print("\n=== Public-read ACL 테스트 ===")

    uploader = S3Uploader()

    # 테스트용 텍스트 파일 생성
    test_content = b"Test content for public access"
    test_key = "test/public_access_test.txt"

    try:
        # Public-read ACL로 업로드 시도
        uploader.s3_client.put_object(
            Bucket=uploader.bucket_name,
            Key=test_key,
            Body=test_content,
            ContentType='text/plain',
            ACL='public-read'
        )

        # 생성된 URL
        public_url = f"https://{uploader.bucket_name}.s3.{settings.AWS_S3_REGION}.amazonaws.com/{test_key}"
        print(f"✅ Public-read ACL 업로드 성공")
        print(f"URL: {public_url}")

        # URL 접근 테스트
        response = requests.get(public_url, timeout=10)
        if response.status_code == 200:
            print("✅ Public URL 접근 성공!")
            print(f"응답 내용: {response.text}")
        else:
            print(f"❌ Public URL 접근 실패: {response.status_code}")
            print(f"응답 내용: {response.text}")

        # 테스트 파일 삭제
        uploader.delete_file(test_key)
        print("✅ 테스트 파일 삭제 완료")

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessControlListNotSupported':
            print("❌ 버킷에서 ACL을 지원하지 않음")
        else:
            print(f"❌ Public-read ACL 업로드 실패: {e}")
    except Exception as e:
        print(f"❌ 테스트 중 오류: {e}")

def suggest_bucket_policy():
    """권장 버킷 정책 출력"""
    print("\n=== 권장 S3 버킷 정책 ===")

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    policy = {
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

    import json
    print("다음 정책을 S3 버킷에 설정하면 public read 접근이 가능합니다:")
    print(json.dumps(policy, indent=2))

def test_existing_image_access():
    """기존 업로드된 이미지 접근 테스트"""
    print("\n=== 기존 이미지 접근 테스트 ===")

    # Django shell에서 기존 팀 멤버 이미지 URL 가져오기
    try:
        from apps.solana_auth.models import TeamMember
        team_members = TeamMember.objects.filter(image_url__isnull=False)[:3]

        for member in team_members:
            if member.image_url and '.amazonaws.com' in member.image_url:
                print(f"\n팀 멤버: {member.position_ko}")
                print(f"원본 URL: {member.image_url}")

                # 직접 접근 테스트
                try:
                    response = requests.get(member.image_url, timeout=10)
                    if response.status_code == 200:
                        print("✅ 직접 접근 성공")
                    else:
                        print(f"❌ 직접 접근 실패: {response.status_code}")
                except Exception as e:
                    print(f"❌ 접근 테스트 오류: {e}")

    except Exception as e:
        print(f"❌ 기존 이미지 테스트 오류: {e}")

if __name__ == "__main__":
    print("S3 Public Access 설정 확인 및 테스트")
    print("="*50)

    test_s3_bucket_policy()
    test_public_read_acl()
    suggest_bucket_policy()
    test_existing_image_access()

    print("\n" + "="*50)
    print("테스트 완료")