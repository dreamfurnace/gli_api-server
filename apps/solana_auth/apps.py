from django.apps import AppConfig
import os


class SolanaAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.solana_auth'
    verbose_name = 'Solana Authentication'

    def ready(self):
        # 개발 환경에서만 더미 사용자 자동 생성
        if os.getenv('DJANGO_ENV', 'development') == 'development':
            self.create_dummy_users()

    def create_dummy_users(self):
        """개발 환경에서 더미 사용자 생성"""
        try:
            from django.core.management import call_command
            from django.db import connection
            from django.db.utils import OperationalError
            
            # 데이터베이스 연결 확인
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
            except OperationalError:
                # 마이그레이션이 아직 완료되지 않았을 수 있음
                return

            # 더미 사용자 생성 (이미 존재하면 스킵)
            call_command('create_dummy_users')
            print("✅ GLI Platform 더미 사용자 확인 완료")
            
        except Exception as e:
            print(f"⚠️ 더미 사용자 생성 중 오류: {e}")
            # 에러가 발생해도 앱 시작을 방해하지 않음