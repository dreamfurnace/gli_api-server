from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from apps.solana_auth.models import SolanaUser
import secrets


class Command(BaseCommand):
    help = 'Create dummy users for GLI Platform development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreate users if they already exist',
        )
        parser.add_argument(
            '--no-wallet',
            action='store_true',
            help='Create admin user without wallet address',
        )

    def handle(self, *args, **options):
        dummy_users = [
            {
                'username': 'member1',
                'email': 'member1@gli.com',
                'password': 'member1!',
                'wallet_address': self.generate_dummy_wallet(),
                'membership_level': 'premium',
                'is_staff': False,
                'is_superuser': False,
                'first_name': '회원',
                'last_name': '1'
            },
            {
                'username': 'member2',
                'email': 'member2@gli.com',
                'password': 'member2!',
                'wallet_address': self.generate_dummy_wallet(),
                'membership_level': 'premium',
                'is_staff': False,
                'is_superuser': False,
                'first_name': '회원',
                'last_name': '2'
            },
            {
                'username': 'member3',
                'email': 'member3@gli.com',
                'password': 'member3!',
                'wallet_address': self.generate_dummy_wallet(),
                'membership_level': 'basic',
                'is_staff': False,
                'is_superuser': False,
                'first_name': '회원',
                'last_name': '3'
            }
        ]

        for user_data in dummy_users:
            email = user_data['email']
            
            # 기존 사용자 확인
            if SolanaUser.objects.filter(email=email).exists():
                if options['force']:
                    SolanaUser.objects.filter(email=email).delete()
                    self.stdout.write(
                        self.style.WARNING(f'Deleted existing user: {email}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'User already exists: {email}. Use --force to recreate.')
                    )
                    continue

            # 사용자 생성
            user = SolanaUser.objects.create(
                username=user_data['username'],
                email=user_data['email'],
                password=make_password(user_data['password']),
                wallet_address=user_data['wallet_address'],
                membership_level=user_data['membership_level'],
                is_staff=user_data['is_staff'],
                is_superuser=user_data['is_superuser'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                is_active=True
            )

            wallet_info = f" (Wallet: {user_data['wallet_address'][:8]}...)" if user_data['wallet_address'] else " (No Wallet)"
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created user: {user.email} ({user.membership_level}){wallet_info}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS('✅ Dummy users creation completed!')
        )

    def generate_dummy_wallet(self):
        """더미 솔라나 지갑 주소 생성"""
        # 실제 솔라나 지갑 형식을 모방한 더미 주소
        return ''.join(secrets.choice('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz') 
                      for _ in range(44))