#!/usr/bin/env python3
"""
S3 연결 테스트 스크립트
"""
import os
import sys
from pathlib import Path

# Django 설정
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from django.conf import settings

def test_s3_connection():
    """S3 연결 테스트"""
    print("🔍 S3 연결 테스트 시작...")

    # 환경변수 확인
    print(f"✅ AWS_ACCESS_KEY_ID: {os.getenv('AWS_ACCESS_KEY_ID', 'NOT_SET')[:10]}...")
    print(f"✅ AWS_SECRET_ACCESS_KEY: {'SET' if os.getenv('AWS_SECRET_ACCESS_KEY') else 'NOT_SET'}")
    print(f"✅ AWS_STORAGE_BUCKET_NAME: {os.getenv('AWS_STORAGE_BUCKET_NAME')}")
    print(f"✅ AWS_S3_REGION: {os.getenv('AWS_S3_REGION')}")

    try:
        # boto3 클라이언트 생성
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_S3_REGION', 'ap-northeast-2')
        )

        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

        print(f"🔍 버킷 '{bucket_name}' 접근 테스트...")

        # 버킷 존재 확인
        response = s3_client.head_bucket(Bucket=bucket_name)
        print(f"✅ 버킷 접근 성공: {bucket_name}")

        # 버킷 내용 조회 (최대 5개)
        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=5)

            if 'Contents' in response:
                print(f"✅ 버킷 내 파일 수: {response.get('KeyCount', 0)}개")
                print("📁 버킷 내 일부 파일:")
                for obj in response['Contents'][:5]:
                    print(f"  - {obj['Key']} (크기: {obj['Size']} bytes)")
            else:
                print("✅ 버킷이 비어있습니다.")

        except ClientError as e:
            print(f"⚠️ 버킷 내용 조회 실패: {e}")

        # 테스트 파일 업로드
        test_content = "S3 연결 테스트 파일"
        test_key = "test/connection_test.txt"

        print(f"🔍 테스트 파일 업로드: {test_key}")

        s3_client.put_object(
            Bucket=bucket_name,
            Key=test_key,
            Body=test_content.encode('utf-8'),
            ContentType='text/plain'
        )

        print(f"✅ 테스트 파일 업로드 성공!")

        # 업로드된 파일 확인
        response = s3_client.head_object(Bucket=bucket_name, Key=test_key)
        print(f"✅ 업로드된 파일 확인 완료 (크기: {response['ContentLength']} bytes)")

        # 파일 URL 생성
        file_url = f"https://{bucket_name}.s3.{os.getenv('AWS_S3_REGION', 'ap-northeast-2')}.amazonaws.com/{test_key}"
        print(f"✅ 파일 URL: {file_url}")

        # 테스트 파일 삭제
        s3_client.delete_object(Bucket=bucket_name, Key=test_key)
        print(f"✅ 테스트 파일 삭제 완료")

        print("🎉 S3 연결 테스트 모두 성공!")
        return True

    except NoCredentialsError:
        print("❌ AWS 자격증명이 설정되지 않았습니다.")
        return False
    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"❌ AWS 클라이언트 오류 ({error_code}): {e}")
        return False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return False

def test_s3uploader_class():
    """S3Uploader 클래스 테스트"""
    print("\n🔍 S3Uploader 클래스 테스트 시작...")

    try:
        from apps.solana_auth.utils.s3_upload import S3Uploader

        uploader = S3Uploader()
        print("✅ S3Uploader 클래스 인스턴스 생성 성공")

        # 테스트용 더미 파일 생성
        import tempfile
        import io
        from django.core.files.uploadedfile import SimpleUploadedFile

        # 테스트 이미지 데이터 (간단한 텍스트 파일로 대체)
        test_content = b"Test image content for S3 upload"
        test_file = SimpleUploadedFile(
            "test_image.jpg",
            test_content,
            content_type="image/jpeg"
        )

        # S3 업로드 테스트
        print("🔍 S3Uploader로 파일 업로드 테스트...")
        result = uploader.upload_file(test_file, 'test')

        if result:
            print(f"✅ S3Uploader 업로드 성공: {result}")
            return True
        else:
            print("❌ S3Uploader 업로드 실패")
            return False

    except ImportError as e:
        print(f"❌ S3Uploader 클래스를 찾을 수 없습니다: {e}")
        return False
    except Exception as e:
        print(f"❌ S3Uploader 테스트 중 오류: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("GLI Platform S3 연결 테스트")
    print("=" * 60)

    # 기본 S3 연결 테스트
    s3_success = test_s3_connection()

    # S3Uploader 클래스 테스트
    uploader_success = test_s3uploader_class()

    print("\n" + "=" * 60)
    print("테스트 결과 요약")
    print("=" * 60)
    print(f"S3 기본 연결: {'✅ 성공' if s3_success else '❌ 실패'}")
    print(f"S3Uploader 클래스: {'✅ 성공' if uploader_success else '❌ 실패'}")

    if s3_success and uploader_success:
        print("🎉 모든 S3 테스트가 성공했습니다!")
        exit(0)
    else:
        print("❌ 일부 테스트가 실패했습니다.")
        exit(1)