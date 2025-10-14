#!/usr/bin/env python3
"""
Django management command를 통한 STG 데이터 이식
"""
import os
import django
import json
from pathlib import Path

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('DJANGO_ENV', 'staging')

django.setup()

from apps.solana_auth.models import SolanaUser

def create_users_from_dump():
    """로컬 덤프 데이터를 기반으로 STG 환경에 사용자 생성"""

    # JSON 파일 로드
    dump_file = Path('local_users_dump.json')
    if not dump_file.exists():
        print("❌ local_users_dump.json 파일을 찾을 수 없습니다.")
        return

    with open(dump_file, 'r', encoding='utf-8') as f:
        users_data = json.load(f)

    print(f"📝 {len(users_data)}명의 사용자 데이터 로드 완료")

    created_count = 0
    updated_count = 0
    error_count = 0

    for user_data in users_data:
        try:
            fields = user_data['fields']

            # 기존 사용자 확인 (이메일 또는 사용자명으로)
            existing_user = None
            if fields.get('email'):
                existing_user = SolanaUser.objects.filter(email=fields['email']).first()
            elif fields.get('username'):
                existing_user = SolanaUser.objects.filter(username=fields['username']).first()

            if existing_user:
                # 기존 사용자 업데이트
                for key, value in fields.items():
                    if key not in ['password', 'groups', 'user_permissions']:
                        setattr(existing_user, key, value)
                existing_user.save()
                print(f"✅ 업데이트: {existing_user.email or existing_user.username}")
                updated_count += 1
            else:
                # 새 사용자 생성
                user_fields = {k: v for k, v in fields.items()
                             if k not in ['groups', 'user_permissions']}

                new_user = SolanaUser.objects.create(**user_fields)
                print(f"🆕 생성: {new_user.email or new_user.username}")
                created_count += 1

        except Exception as e:
            print(f"❌ 오류 발생 ({fields.get('email', fields.get('username', 'Unknown'))}): {e}")
            error_count += 1

    print(f"\n=== 결과 ===")
    print(f"✅ 생성: {created_count}명")
    print(f"🔄 업데이트: {updated_count}명")
    print(f"❌ 오류: {error_count}명")
    print(f"📊 전체: {created_count + updated_count + error_count}명 처리")

if __name__ == '__main__':
    print("=== STG 환경으로 사용자 데이터 이식 시작 ===")
    create_users_from_dump()
    print("=== 데이터 이식 완료 ===")