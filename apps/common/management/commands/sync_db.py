"""
Staging RDS와 로컬 PostgreSQL DB 동기화

사용법:
    # Staging에서 데이터 덤프하여 S3에 업로드
    DJANGO_ENV=staging python manage.py sync_db --dump

    # 로컬에서 S3에서 다운로드하여 복원
    DJANGO_ENV=development python manage.py sync_db --load

    # 백업 생성 (로컬 데이터 보호)
    python manage.py sync_db --backup
"""

import os
import json
import gzip
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from django.db import connection

import boto3
from botocore.exceptions import ClientError


class Command(BaseCommand):
    help = 'Staging RDS와 로컬 DB 동기화'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dump',
            action='store_true',
            help='현재 DB를 덤프하여 S3에 업로드 (staging에서 실행)'
        )
        parser.add_argument(
            '--load',
            action='store_true',
            help='S3에서 다운로드하여 현재 DB에 복원 (local에서 실행)'
        )
        parser.add_argument(
            '--backup',
            action='store_true',
            help='현재 로컬 DB 백업'
        )
        parser.add_argument(
            '--s3-key',
            type=str,
            default='db-sync/latest-dump.json.gz',
            help='S3 객체 키 (기본값: db-sync/latest-dump.json.gz)'
        )
        parser.add_argument(
            '--exclude',
            type=str,
            nargs='+',
            default=['contenttypes', 'auth.permission', 'sessions.session'],
            help='제외할 앱/모델 (기본값: contenttypes, auth.permission, sessions.session)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='확인 없이 실행'
        )

    def handle(self, *args, **options):
        self.s3_key = options['s3_key']
        self.exclude = options['exclude']
        self.force = options['force']

        # S3 클라이언트 초기화
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

        if options['dump']:
            self.dump_and_upload()
        elif options['load']:
            self.download_and_load()
        elif options['backup']:
            self.backup_local_db()
        else:
            raise CommandError('--dump, --load, --backup 중 하나를 선택하세요')

    def dump_and_upload(self):
        """현재 DB를 덤프하여 S3에 업로드"""
        django_env = os.getenv('DJANGO_ENV', 'unknown')
        self.stdout.write(self.style.WARNING(f'📤 {django_env} DB 덤프 시작...'))

        # 임시 파일 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_file = f'/tmp/db_dump_{timestamp}.json'

        try:
            # Django dumpdata 실행
            self.stdout.write('🔄 데이터 추출 중...')
            with open(temp_file, 'w', encoding='utf-8') as f:
                call_command(
                    'dumpdata',
                    exclude=self.exclude,
                    indent=2,
                    stdout=f,
                    verbosity=0
                )

            # gzip 압축
            self.stdout.write('🗜️  압축 중...')
            gz_file = f'{temp_file}.gz'
            with open(temp_file, 'rb') as f_in:
                with gzip.open(gz_file, 'wb') as f_out:
                    f_out.writelines(f_in)

            # 파일 크기 확인
            original_size = os.path.getsize(temp_file)
            compressed_size = os.path.getsize(gz_file)
            self.stdout.write(
                f'📊 원본: {original_size / 1024 / 1024:.2f} MB → '
                f'압축: {compressed_size / 1024 / 1024:.2f} MB '
                f'({compressed_size / original_size * 100:.1f}%)'
            )

            # S3 업로드
            self.stdout.write(f'☁️  S3 업로드 중: s3://{self.bucket_name}/{self.s3_key}')
            with open(gz_file, 'rb') as f:
                self.s3_client.upload_fileobj(
                    f,
                    self.bucket_name,
                    self.s3_key,
                    ExtraArgs={
                        'Metadata': {
                            'source_env': django_env,
                            'dump_timestamp': timestamp,
                            'django_version': str(settings.VERSION) if hasattr(settings, 'VERSION') else 'unknown'
                        }
                    }
                )

            # 타임스탬프별 백업도 저장
            backup_key = f'db-sync/backups/dump_{timestamp}.json.gz'
            with open(gz_file, 'rb') as f:
                self.s3_client.upload_fileobj(f, self.bucket_name, backup_key)

            self.stdout.write(self.style.SUCCESS(
                f'✅ 덤프 완료!\n'
                f'   - Latest: s3://{self.bucket_name}/{self.s3_key}\n'
                f'   - Backup: s3://{self.bucket_name}/{backup_key}'
            ))

        except Exception as e:
            raise CommandError(f'덤프 실패: {e}')
        finally:
            # 임시 파일 삭제
            for f in [temp_file, f'{temp_file}.gz']:
                if os.path.exists(f):
                    os.remove(f)

    def download_and_load(self):
        """S3에서 다운로드하여 현재 DB에 복원"""
        django_env = os.getenv('DJANGO_ENV', 'unknown')
        if django_env != 'development':
            raise CommandError('⚠️  이 명령은 development 환경에서만 실행하세요!')

        # 확인
        if not self.force:
            confirm = input(
                self.style.WARNING(
                    '\n⚠️  경고: 현재 로컬 DB의 모든 데이터가 삭제되고 Staging 데이터로 대체됩니다.\n'
                    '계속하시겠습니까? (yes/no): '
                )
            )
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.ERROR('취소되었습니다.'))
                return

        self.stdout.write(self.style.WARNING('📥 Staging DB 다운로드 및 복원 시작...'))

        # 로컬 DB 백업
        self.stdout.write('💾 로컬 DB 백업 중...')
        self.backup_local_db(auto=True)

        # 임시 파일 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        gz_file = f'/tmp/db_restore_{timestamp}.json.gz'
        json_file = f'/tmp/db_restore_{timestamp}.json'

        try:
            # S3에서 다운로드
            self.stdout.write(f'☁️  S3 다운로드 중: s3://{self.bucket_name}/{self.s3_key}')
            with open(gz_file, 'wb') as f:
                self.s3_client.download_fileobj(self.bucket_name, self.s3_key, f)

            # 압축 해제
            self.stdout.write('🗜️  압축 해제 중...')
            with gzip.open(gz_file, 'rb') as f_in:
                with open(json_file, 'wb') as f_out:
                    f_out.write(f_in.read())

            # 파일 크기 확인
            file_size = os.path.getsize(json_file)
            self.stdout.write(f'📊 다운로드 완료: {file_size / 1024 / 1024:.2f} MB')

            # DB 초기화 (기존 데이터 삭제)
            self.stdout.write(self.style.WARNING('🗑️  기존 데이터 삭제 중...'))
            self.flush_database()

            # 데이터 로드
            self.stdout.write('🔄 데이터 복원 중...')
            call_command('loaddata', json_file, verbosity=2)

            self.stdout.write(self.style.SUCCESS('✅ 복원 완료!'))

        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise CommandError(
                    f'S3에 덤프 파일이 없습니다: s3://{self.bucket_name}/{self.s3_key}\n'
                    'Staging 환경에서 먼저 --dump를 실행하세요.'
                )
            raise CommandError(f'S3 다운로드 실패: {e}')
        except Exception as e:
            raise CommandError(f'복원 실패: {e}')
        finally:
            # 임시 파일 삭제
            for f in [gz_file, json_file]:
                if os.path.exists(f):
                    os.remove(f)

    def backup_local_db(self, auto=False):
        """로컬 DB 백업"""
        if not auto:
            self.stdout.write(self.style.WARNING('💾 로컬 DB 백업 시작...'))

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = Path(settings.BASE_DIR) / 'backups'
        backup_dir.mkdir(exist_ok=True)

        backup_file = backup_dir / f'local_backup_{timestamp}.json'

        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                call_command(
                    'dumpdata',
                    exclude=self.exclude,
                    indent=2,
                    stdout=f,
                    verbosity=0
                )

            file_size = os.path.getsize(backup_file)
            self.stdout.write(self.style.SUCCESS(
                f'✅ 백업 완료: {backup_file} ({file_size / 1024 / 1024:.2f} MB)'
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'백업 실패: {e}'))

    def flush_database(self):
        """데이터베이스 초기화 (테이블은 유지, 데이터만 삭제)"""
        with connection.cursor() as cursor:
            # 모든 테이블 찾기
            cursor.execute("""
                SELECT tablename FROM pg_tables
                WHERE schemaname = 'public'
            """)
            tables = [row[0] for row in cursor.fetchall()]

            # 외래 키 제약 조건 임시 비활성화
            for table in tables:
                cursor.execute(f'TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE')
