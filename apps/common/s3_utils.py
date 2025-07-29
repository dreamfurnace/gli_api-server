import boto3
from django.conf import settings
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)

def upload_to_s3(file_buffer, file_name, folder_name=''):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION
    )
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    # 폴더명(prefix) 설정
    if folder_name:
        s3_file_key = f"{folder_name}/{uuid4()}_{file_name}"
    else:
        s3_file_key = f"{uuid4()}_{file_name}"

    try:
        file_buffer.seek(0)
        s3_client.upload_fileobj(
            file_buffer,
            bucket_name,
            s3_file_key,
            ExtraArgs={'ACL': 'private'}
        )
        s3_url = f"https://{bucket_name}.s3.{settings.AWS_S3_REGION}.amazonaws.com/{s3_file_key}"
        logger.info(f"S3 upload success: {s3_url}")
        return s3_url
    except Exception as e:
        logger.error(f"S3 upload error: {e}", exc_info=True)
        return None
