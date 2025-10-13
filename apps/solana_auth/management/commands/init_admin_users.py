#!/usr/bin/env python
"""
Django management command to initialize AdminUser records for staff SolanaUsers.

Usage:
    python manage.py init_admin_users
"""
from django.core.management.base import BaseCommand
from apps.solana_auth.models import SolanaUser, AdminUser, AdminGrade


class Command(BaseCommand):
    help = 'Initialize AdminUser records for staff SolanaUsers'

    def handle(self, *args, **options):
        # Create AdminGrades if they don't exist
        super_admin_grade, created = AdminGrade.objects.get_or_create(
            name="슈퍼 관리자",
            defaults={"description": "모든 권한을 가진 최고 관리자"}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ Created AdminGrade: {super_admin_grade.name}'))
        else:
            self.stdout.write(f'   ⏭️  AdminGrade already exists: {super_admin_grade.name}')

        normal_admin_grade, created = AdminGrade.objects.get_or_create(
            name="일반 관리자",
            defaults={"description": "제한된 권한을 가진 일반 관리자"}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ Created AdminGrade: {normal_admin_grade.name}'))
        else:
            self.stdout.write(f'   ⏭️  AdminGrade already exists: {normal_admin_grade.name}')

        # Find staff users
        staff_users = SolanaUser.objects.filter(is_staff=True)
        self.stdout.write(self.style.WARNING(f'\n📦 Found {staff_users.count()} staff users'))

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for user in staff_users:
            # Check if AdminUser already exists
            if hasattr(user, 'admin_profile'):
                self.stdout.write(f'   ⏭️  AdminUser already exists for: {user.username}')
                skipped_count += 1
                continue

            # Determine grade based on is_superuser
            grade = super_admin_grade if user.is_superuser else normal_admin_grade

            # Create AdminUser
            AdminUser.objects.create(
                user=user,
                grade=grade,
                is_active=user.is_active
            )
            self.stdout.write(self.style.SUCCESS(
                f'   ✅ Created AdminUser for: {user.username} (Grade: {grade.name})'
            ))
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ AdminUsers: {created_count} created, {skipped_count} skipped'
        ))
