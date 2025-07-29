from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import SolanaUser


class SolanaAuthMiddleware(MiddlewareMixin):
    """Solana 지갑 기반 JWT 인증 미들웨어"""
    
    def process_request(self, request):
        # Authorization 헤더에서 토큰 추출
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
            try:
                # JWT 토큰 검증
                validated_token = UntypedToken(token)
                
                # 토큰에서 지갑 주소 추출
                wallet_address = validated_token.get('wallet_address')
                user_id = validated_token.get('user_id')
                
                if wallet_address and user_id:
                    try:
                        # 사용자 조회
                        user = SolanaUser.objects.get(
                            id=user_id, 
                            wallet_address=wallet_address
                        )
                        
                        # request 객체에 사용자 정보 추가
                        request.solana_user = user
                        request.wallet_address = wallet_address
                        
                        # Django의 기본 user 객체에도 정보 추가 (기존 시스템과의 호환성)
                        class MockUser:
                            def __init__(self, solana_user):
                                self.id = solana_user.id
                                self.username = solana_user.username
                                self.wallet_address = solana_user.wallet_address
                                self.is_authenticated = True
                                self.is_active = solana_user.is_active
                        
                        request.user = MockUser(user)
                        
                    except SolanaUser.DoesNotExist:
                        pass
                        
            except (InvalidToken, TokenError):
                pass
        
        return None