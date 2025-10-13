#!/usr/bin/env python
"""
더미 사용자 생성 스크립트
Frontend 로그인 화면의 3개 더미 계정을 데이터베이스에 생성합니다.
"""

import os
import sys
import django

# Django 프로젝트 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.solana_auth.models import SolanaUser
from django.contrib.auth.hashers import make_password

def create_dummy_users():
    """더미 사용자 3개 생성"""

    dummy_users = [
        {
            'username': 'member1',
            'email': 'member1@gli.com',
            'password': 'member1!',
            'is_staff': False,
            'is_superuser': False,
            'membership_level': 'premium',
            'first_name': '회원',
            'last_name': '1',
            'description': '회원1'
        },
        {
            'username': 'member2',
            'email': 'member2@gli.com',
            'password': 'member2!',
            'is_staff': False,
            'is_superuser': False,
            'membership_level': 'premium',
            'first_name': '회원',
            'last_name': '2',
            'description': '회원2'
        },
        {
            'username': 'member3',
            'email': 'member3@gli.com',
            'password': 'member3!',
            'is_staff': False,
            'is_superuser': False,
            'membership_level': 'basic',
            'first_name': '회원',
            'last_name': '3',
            'description': '회원3'
        }
    ]

    print("🚀 GLI Platform - 더미 사용자 생성 시작\n")

    for user_data in dummy_users:
        username = user_data['username']

        # 기존 사용자가 있는지 확인
        if SolanaUser.objects.filter(username=username).exists():
            print(f"⚠️  {user_data['description']} ({username}) - 이미 존재함")
            continue

        # 사용자 생성
        try:
            user = SolanaUser.objects.create(
                username=username,
                email=user_data['email'],
                password=make_password(user_data['password']),
                is_staff=user_data['is_staff'],
                is_superuser=user_data['is_superuser'],
                membership_level=user_data['membership_level'],
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', ''),
                is_active=True
            )

            print(f"✅ {user_data['description']} ({username}) - 생성 완료")

        except Exception as e:
            print(f"❌ {user_data['description']} ({username}) - 생성 실패: {e}")

    print(f"\n📊 생성된 사용자 수: {SolanaUser.objects.count()}명")
    print("\n🎉 더미 사용자 생성 완료!")
    print("\n💡 로그인 테스트:")
    print("   - 회원1: member1@gli.com / member1!")
    print("   - 회원2: member2@gli.com / member2!")
    print("   - 회원3: member3@gli.com / member3!")

if __name__ == '__main__':
    create_dummy_users()