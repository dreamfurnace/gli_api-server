# apps/solana_auth/utils/s3_upload.py
import boto3
import os
import uuid
from datetime import datetime
from django.conf import settings
from botocore.exceptions import ClientError


class S3Uploader:
    """AWS S3 파일 업로드 유틸리티"""

    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_file(self, file, folder='uploads'):
        """
        파일을 S3에 업로드

        Args:
            file: Django UploadedFile 객체
            folder: S3 내 폴더 경로 (기본값: 'uploads')

        Returns:
            dict: {'url': S3 URL, 'key': S3 객체 키}
        """
        try:
            # 파일 확장자 추출
            file_ext = os.path.splitext(file.name)[1]

            # 고유한 파일명 생성 (UUID + timestamp)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{uuid.uuid4().hex}_{timestamp}{file_ext}"

            # S3 객체 키 생성
            s3_key = f"{folder}/{unique_filename}"

            # Content-Type 설정
            content_type = file.content_type or 'application/octet-stream'

            # S3에 업로드 (버킷 정책을 통해 퍼블릭 접근 관리)
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': content_type,
                }
            )

            # S3 URL 생성
            file_url = f"https://{self.bucket_name}.s3.{settings.AWS_S3_REGION}.amazonaws.com/{s3_key}"

            return {
                'url': file_url,
                'key': s3_key,
                'filename': file.name,
                'size': file.size,
                'content_type': content_type
            }

        except ClientError as e:
            raise Exception(f"S3 업로드 실패: {str(e)}")
        except Exception as e:
            raise Exception(f"파일 업로드 중 오류 발생: {str(e)}")

    def delete_file(self, s3_key):
        """
        S3에서 파일 삭제

        Args:
            s3_key: S3 객체 키

        Returns:
            bool: 삭제 성공 여부
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return True
        except ClientError as e:
            raise Exception(f"S3 파일 삭제 실패: {str(e)}")

    def generate_presigned_url(self, s3_key, expiration=3600):
        """
        미리 서명된 URL 생성 (임시 접근 URL)

        Args:
            s3_key: S3 객체 키
            expiration: URL 유효 시간 (초, 기본값: 3600초 = 1시간)

        Returns:
            str: 미리 서명된 URL
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            raise Exception(f"Presigned URL 생성 실패: {str(e)}")
