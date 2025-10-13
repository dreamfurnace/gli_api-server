#!/usr/bin/env python
"""
Django management command to clear all users from the database.

Usage:
    python manage.py clear_users
    python manage.py clear_users --confirm
"""
from django.core.management.base import BaseCommand, CommandError
from apps.solana_auth.models import SolanaUser, AdminUser


class Command(BaseCommand):
    help = 'Clear all users from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without prompt',
        )

    def handle(self, *args, **options):
        confirm = options['confirm']

        # Count users
        solana_count = SolanaUser.objects.count()
        admin_count = AdminUser.objects.count()

        self.stdout.write(self.style.WARNING(
            f'⚠️  About to delete {solana_count} SolanaUsers and {admin_count} AdminUsers'
        ))

        if not confirm:
            response = input('Are you sure you want to delete all users? Type "yes" to confirm: ')
            if response.lower() != 'yes':
                self.stdout.write(self.style.ERROR('❌ Operation cancelled'))
                return

        # Delete users
        SolanaUser.objects.all().delete()
        AdminUser.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            f'✅ Deleted {solana_count} SolanaUsers and {admin_count} AdminUsers'
        ))
