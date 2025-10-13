#!/usr/bin/env python
"""
Django management command to migrate data from SQLite backup to PostgreSQL.

Usage:
    python manage.py migrate_from_sqlite --file=/path/to/backup.json
    python manage.py migrate_from_sqlite --s3-key=db-backup/gli_data_backup.json
"""
import json
import boto3
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth import get_user_model
from apps.solana_auth.models import Member

User = get_user_model()


class Command(BaseCommand):
    help = 'Migrate data from SQLite JSON backup to PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to local JSON backup file',
        )
        parser.add_argument(
            '--s3-key',
            type=str,
            help='S3 key of JSON backup file (bucket: gli-platform-media-dev)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview changes without committing',
        )

    def handle(self, *args, **options):
        # Load data
        if options['s3_key']:
            self.stdout.write(self.style.WARNING(f"Loading from S3: {options['s3_key']}"))
            data = self.load_from_s3(options['s3_key'])
        elif options['file']:
            self.stdout.write(self.style.WARNING(f"Loading from file: {options['file']}"))
            data = self.load_from_file(options['file'])
        else:
            raise CommandError('Must provide either --file or --s3-key')

        dry_run = options['dry_run']
        if dry_run:
            self.stdout.write(self.style.WARNING('🧪 DRY RUN MODE - No data will be committed'))

        # Migrate data
        try:
            with transaction.atomic():
                self.migrate_users(data.get('users', []), dry_run)
                self.migrate_members(data.get('members', []), dry_run)

                if dry_run:
                    raise Exception('Dry run - rolling back transaction')

        except Exception as e:
            if dry_run:
                self.stdout.write(self.style.SUCCESS('✅ Dry run completed successfully'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ Migration failed: {e}'))
                raise

        self.stdout.write(self.style.SUCCESS('🎉 Migration completed successfully!'))

    def load_from_file(self, file_path):
        """Load JSON data from local file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise CommandError(f'File not found: {file_path}')
        except json.JSONDecodeError as e:
            raise CommandError(f'Invalid JSON: {e}')

    def load_from_s3(self, s3_key):
        """Load JSON data from S3"""
        try:
            s3 = boto3.client('s3')
            response = s3.get_object(Bucket='gli-platform-media-dev', Key=s3_key)
            data = response['Body'].read().decode('utf-8')
            return json.load(data)
        except Exception as e:
            raise CommandError(f'Failed to load from S3: {e}')

    def migrate_users(self, users_data, dry_run=False):
        """Migrate User (admin) data"""
        self.stdout.write(self.style.MIGRATE_HEADING(f'\n📦 Migrating {len(users_data)} admin users...'))

        created = 0
        updated = 0
        skipped = 0

        for user_data in users_data:
            username = user_data.get('username')
            email = user_data.get('email')

            if not username:
                self.stdout.write(self.style.WARNING(f'⚠️  Skipping user without username: {user_data}'))
                skipped += 1
                continue

            # Check if user exists
            existing_user = User.objects.filter(username=username).first()

            if existing_user:
                self.stdout.write(f'   ⏭️  User already exists: {username}')
                updated += 1
            else:
                if not dry_run:
                    User.objects.create(
                        username=username,
                        email=email or f'{username}@gli.com',
                        first_name=user_data.get('first_name', ''),
                        last_name=user_data.get('last_name', ''),
                        is_staff=user_data.get('is_staff', False),
                        is_superuser=user_data.get('is_superuser', False),
                        is_active=user_data.get('is_active', True),
                    )
                self.stdout.write(self.style.SUCCESS(f'   ✅ Created user: {username}'))
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Users: {created} created, {updated} updated, {skipped} skipped'
        ))

    def migrate_members(self, members_data, dry_run=False):
        """Migrate Member data"""
        self.stdout.write(self.style.MIGRATE_HEADING(f'\n📦 Migrating {len(members_data)} members...'))

        created = 0
        updated = 0
        skipped = 0

        for member_data in members_data:
            username = member_data.get('username')
            email = member_data.get('email')

            if not username:
                self.stdout.write(self.style.WARNING(f'⚠️  Skipping member without username: {member_data}'))
                skipped += 1
                continue

            # Check if member exists
            existing_member = Member.objects.filter(username=username).first()

            if existing_member:
                self.stdout.write(f'   ⏭️  Member already exists: {username}')
                updated += 1
            else:
                if not dry_run:
                    Member.objects.create(
                        username=username,
                        email=email or f'{username}@user.gli.com',
                        wallet_address=member_data.get('wallet_address'),
                        membership_level=member_data.get('membership_level', 'basic'),
                        sol_balance=member_data.get('sol_balance', '0.000000000'),
                        is_active=member_data.get('is_active', True),
                        vpx_verify=member_data.get('vpx_verify', 0),
                        vpx_partner=member_data.get('vpx_partner', 0),
                        vpx_experience=member_data.get('vpx_experience', 0),
                        first_name=member_data.get('first_name', ''),
                        last_name=member_data.get('last_name', ''),
                    )
                self.stdout.write(self.style.SUCCESS(f'   ✅ Created member: {username}'))
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Members: {created} created, {updated} updated, {skipped} skipped'
        ))
