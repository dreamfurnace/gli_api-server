#!/usr/bin/env python
"""
관리자 계정 생성 스크립트
슈퍼 관리자 2개, 일반 관리자 2개 생성
"""
import os
import sys
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.solana_auth.models import SolanaUser, AdminGrade, AdminUser

def create_admin_accounts():
    """관리자 계정 생성"""

    # 1. 관리자 등급 생성 또는 가져오기
    super_admin_grade, created = AdminGrade.objects.get_or_create(
        name='슈퍼 관리자',
        defaults={'description': '모든 권한을 가진 최고 관리자'}
    )
    if created:
        print(f'✅ 슈퍼 관리자 등급 생성: {super_admin_grade.name}')
    else:
        print(f'📝 슈퍼 관리자 등급 이미 존재: {super_admin_grade.name}')

    regular_admin_grade, created = AdminGrade.objects.get_or_create(
        name='일반 관리자',
        defaults={'description': '제한된 권한을 가진 일반 관리자'}
    )
    if created:
        print(f'✅ 일반 관리자 등급 생성: {regular_admin_grade.name}')
    else:
        print(f'📝 일반 관리자 등급 이미 존재: {regular_admin_grade.name}')

    # 2. 슈퍼 관리자 계정 생성
    super_admins = [
        {
            'username': 'superadmin1',
            'email': 'superadmin1@gli.com',
            'password': 'super1234!',
            'first_name': '슈퍼',
            'last_name': '관리자1',
        },
        {
            'username': 'superadmin2',
            'email': 'superadmin2@gli.com',
            'password': 'super1234!',
            'first_name': '슈퍼',
            'last_name': '관리자2',
        },
    ]

    for admin_data in super_admins:
        username = admin_data['username']

        # SolanaUser 생성 또는 가져오기
        user, created = SolanaUser.objects.get_or_create(
            username=username,
            defaults={
                'email': admin_data['email'],
                'first_name': admin_data['first_name'],
                'last_name': admin_data['last_name'],
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )

        if created:
            user.set_password(admin_data['password'])
            user.save()
            print(f'✅ SolanaUser 생성: {username}')
        else:
            print(f'📝 SolanaUser 이미 존재: {username}')
            # 비밀번호 업데이트
            user.set_password(admin_data['password'])
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            print(f'🔄 SolanaUser 업데이트: {username}')

        # AdminUser 생성 또는 가져오기
        admin_user, created = AdminUser.objects.get_or_create(
            user=user,
            defaults={
                'grade': super_admin_grade,
                'is_active': True,
            }
        )

        if created:
            print(f'✅ AdminUser 생성: {username} ({super_admin_grade.name})')
        else:
            # 등급 업데이트
            admin_user.grade = super_admin_grade
            admin_user.is_active = True
            admin_user.save()
            print(f'🔄 AdminUser 업데이트: {username} ({super_admin_grade.name})')

    # 3. 일반 관리자 계정 생성
    regular_admins = [
        {
            'username': 'admin1',
            'email': 'admin1@gli.com',
            'password': 'admin1234!',
            'first_name': '일반',
            'last_name': '관리자1',
        },
        {
            'username': 'admin2',
            'email': 'admin2@gli.com',
            'password': 'admin1234!',
            'first_name': '일반',
            'last_name': '관리자2',
        },
    ]

    for admin_data in regular_admins:
        username = admin_data['username']

        # SolanaUser 생성 또는 가져오기
        user, created = SolanaUser.objects.get_or_create(
            username=username,
            defaults={
                'email': admin_data['email'],
                'first_name': admin_data['first_name'],
                'last_name': admin_data['last_name'],
                'is_staff': True,
                'is_superuser': False,
                'is_active': True,
            }
        )

        if created:
            user.set_password(admin_data['password'])
            user.save()
            print(f'✅ SolanaUser 생성: {username}')
        else:
            print(f'📝 SolanaUser 이미 존재: {username}')
            # 비밀번호 업데이트
            user.set_password(admin_data['password'])
            user.is_staff = True
            user.is_superuser = False
            user.is_active = True
            user.save()
            print(f'🔄 SolanaUser 업데이트: {username}')

        # AdminUser 생성 또는 가져오기
        admin_user, created = AdminUser.objects.get_or_create(
            user=user,
            defaults={
                'grade': regular_admin_grade,
                'is_active': True,
            }
        )

        if created:
            print(f'✅ AdminUser 생성: {username} ({regular_admin_grade.name})')
        else:
            # 등급 업데이트
            admin_user.grade = regular_admin_grade
            admin_user.is_active = True
            admin_user.save()
            print(f'🔄 AdminUser 업데이트: {username} ({regular_admin_grade.name})')

    print('\n' + '='*60)
    print('🎉 관리자 계정 생성 완료!')
    print('='*60)
    print('\n슈퍼 관리자 계정:')
    print('  1. superadmin1@gli.com / super1234!')
    print('  2. superadmin2@gli.com / super1234!')
    print('\n일반 관리자 계정:')
    print('  1. admin1@gli.com / admin1234!')
    print('  2. admin2@gli.com / admin1234!')
    print('='*60)

if __name__ == '__main__':
    create_admin_accounts()
