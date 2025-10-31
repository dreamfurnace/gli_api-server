#!/usr/bin/env python
"""
Django management command to create test admin accounts.

Usage:
    python manage.py create_test_accounts
    python manage.py create_test_accounts --reset  # Reset existing passwords
"""
from django.core.management.base import BaseCommand
from apps.solana_auth.models import SolanaUser, AdminUser, AdminGrade


class Command(BaseCommand):
    help = 'Create or update test admin accounts for GLI Platform'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset passwords for existing users',
        )

    def handle(self, *args, **options):
        reset_passwords = options.get('reset', False)

        self.stdout.write(self.style.WARNING('🚀 GLI Platform 테스트 계정 생성 시작...\n'))

        # Create AdminGrades
        super_admin_grade, created = AdminGrade.objects.get_or_create(
            name="슈퍼 관리자",
            defaults={
                "description": "모든 권한을 가진 슈퍼 관리자",
                "permissions": {"all": True}
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ AdminGrade 생성: {super_admin_grade.name}'))

        admin_grade, created = AdminGrade.objects.get_or_create(
            name="일반 관리자",
            defaults={
                "description": "일반 관리 권한",
                "permissions": {"view": True, "edit": True}
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ AdminGrade 생성: {admin_grade.name}'))

        self.stdout.write('')

        # Test accounts configuration
        test_accounts = [
            {
                "username": "superadmin1",
                "email": "superadmin1@gli.com",
                "password": "super1234!",
                "first_name": "슈퍼",
                "last_name": "관리자1",
                "is_staff": True,
                "is_superuser": True,
                "membership_level": "vip",
                "grade": super_admin_grade
            },
            {
                "username": "superadmin2",
                "email": "superadmin2@gli.com",
                "password": "super1234!",
                "first_name": "슈퍼",
                "last_name": "관리자2",
                "is_staff": True,
                "is_superuser": True,
                "membership_level": "vip",
                "grade": super_admin_grade
            },
            {
                "username": "admin1",
                "email": "admin1@gli.com",
                "password": "admin1234!",
                "first_name": "일반",
                "last_name": "관리자1",
                "is_staff": True,
                "is_superuser": False,
                "membership_level": "basic",
                "grade": admin_grade
            },
            {
                "username": "admin2",
                "email": "admin2@gli.com",
                "password": "admin1234!",
                "first_name": "일반",
                "last_name": "관리자2",
                "is_staff": True,
                "is_superuser": False,
                "membership_level": "basic",
                "grade": admin_grade
            }
        ]

        created_count = 0
        updated_count = 0

        for account in test_accounts:
            email = account['email']
            username = account['username']
            password = account.pop('password')
            grade = account.pop('grade')

            try:
                # Try to get existing user
                user = SolanaUser.objects.get(email=email)

                # Update password if reset flag is set
                if reset_passwords:
                    user.set_password(password)
                    user.is_active = True
                    user.is_staff = account['is_staff']
                    user.is_superuser = account['is_superuser']
                    user.membership_level = account['membership_level']
                    user.save()

                    # Update or create AdminUser
                    admin_user, created = AdminUser.objects.get_or_create(
                        user=user,
                        defaults={"grade": grade, "is_active": True}
                    )
                    if not created:
                        admin_user.grade = grade
                        admin_user.is_active = True
                        admin_user.save()

                    self.stdout.write(self.style.SUCCESS(
                        f'✅ 계정 업데이트: {email} / {password}'
                    ))
                    updated_count += 1
                else:
                    self.stdout.write(self.style.WARNING(
                        f'⏭️  이미 존재하는 계정 (--reset으로 비밀번호 재설정 가능): {email}'
                    ))

            except SolanaUser.DoesNotExist:
                # Create new user
                user = SolanaUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=account['first_name'],
                    last_name=account['last_name'],
                    is_staff=account['is_staff'],
                    is_superuser=account['is_superuser'],
                    membership_level=account['membership_level'],
                    is_active=True
                )

                # Create AdminUser
                AdminUser.objects.create(
                    user=user,
                    grade=grade,
                    is_active=True
                )

                self.stdout.write(self.style.SUCCESS(
                    f'✨ 새 계정 생성: {email} / {password}'
                ))
                created_count += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎉 완료!'))
        self.stdout.write(f'   생성: {created_count}개')
        self.stdout.write(f'   업데이트: {updated_count}개')

        self.stdout.write('')
        self.stdout.write(self.style.WARNING('📋 테스트 계정 목록:'))
        self.stdout.write('   슈퍼 관리자:')
        self.stdout.write('     • superadmin1@gli.com / super1234!')
        self.stdout.write('     • superadmin2@gli.com / super1234!')
        self.stdout.write('   일반 관리자:')
        self.stdout.write('     • admin1@gli.com / admin1234!')
        self.stdout.write('     • admin2@gli.com / admin1234!')
        self.stdout.write('')
