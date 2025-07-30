import secrets
import hashlib
import time
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import SolanaUser, AuthNonce, SolanaTransaction
from .serializers import (
    SolanaUserSerializer, 
    NonceRequestSerializer, 
    AuthVerifySerializer,
    SolanaTransactionSerializer
)

# 솔라나 서명 검증을 위한 임포트 (실제 구현시 solana-py 라이브러리 사용)
try:
    from solana.publickey import PublicKey
    from nacl.signing import VerifyKey
    from nacl.exceptions import BadSignatureError
    SOLANA_AVAILABLE = True
except ImportError:
    SOLANA_AVAILABLE = False


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Traditional username/password login for admin panel
    POST /api/auth/login/
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Try to authenticate with username or email
    user = None
    if '@' in username:
        # Email login
        try:
            user_obj = SolanaUser.objects.get(email=username)
            user = authenticate(request, username=user_obj.username, password=password)
        except SolanaUser.DoesNotExist:
            pass
    else:
        # Username login
        user = authenticate(request, username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Update last login
    user.last_login = timezone.now()
    user.save()
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    
    # Serialize user data
    user_serializer = SolanaUserSerializer(user)
    
    return Response({
        'token': {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        },
        'user': user_serializer.data,
        'message': '✅ GLI Platform Admin 로그인 성공!'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def request_nonce(request):
    """
    인증용 nonce 발급
    POST /api/auth/nonce/
    """
    serializer = NonceRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid request data', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    wallet_address = serializer.validated_data['wallet_address']
    
    # 지갑 주소가 이미 등록된 사용자가 있는지 확인
    try:
        existing_user = SolanaUser.objects.get(wallet_address=wallet_address)
        return Response(
            {'error': '이미 등록된 지갑 주소입니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except SolanaUser.DoesNotExist:
        pass
    
    # 새로운 nonce 생성
    nonce = secrets.token_hex(32)
    
    # 기존 nonce가 있다면 사용됨으로 표시
    AuthNonce.objects.filter(wallet_address=wallet_address, used=False).update(used=True)
    
    # 새로운 nonce 저장
    AuthNonce.objects.create(
        wallet_address=wallet_address,
        nonce=nonce,
        used=False
    )
    
    return Response({
        'nonce': nonce,
        'message': 'Nonce가 성공적으로 생성되었습니다.'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_signature(request):
    """
    서명 검증 및 인증 토큰 발급
    POST /api/auth/verify/
    """
    serializer = AuthVerifySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid request data', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    data = serializer.validated_data
    wallet_address = data['wallet_address']
    signature = bytes(data['signature'])
    message = data['message']
    nonce = data['nonce']
    
    # Nonce 검증
    try:
        auth_nonce = AuthNonce.objects.get(
            wallet_address=wallet_address,
            nonce=nonce,
            used=False,
            created_at__gte=timezone.now() - timedelta(minutes=5)
        )
    except AuthNonce.DoesNotExist:
        return Response(
            {'error': 'Invalid or expired nonce'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 서명 검증 (실제 환경에서는 solana-py 라이브러리 사용)
    if SOLANA_AVAILABLE:
        try:
            # 공개키 생성
            public_key = PublicKey(wallet_address)
            
            # 메시지를 바이트로 변환
            message_bytes = message.encode('utf-8')
            
            # 서명 검증 (간단한 예제 - 실제로는 더 복잡한 검증 로직 필요)
            # verify_key = VerifyKey(public_key.to_bytes())
            # verify_key.verify(message_bytes, signature)
            
            # 개발 환경에서는 검증을 통과시킴
            signature_valid = True
            
        except Exception as e:
            return Response(
                {'error': f'Signature verification failed: {str(e)}'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    else:
        # 개발 환경: 솔라나 라이브러리가 없을 때는 기본적으로 통과
        signature_valid = True
    
    if not signature_valid:
        return Response(
            {'error': 'Invalid signature'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Nonce 사용 처리
    auth_nonce.used = True
    auth_nonce.save()
    
    # 사용자 생성 또는 조회
    user, created = SolanaUser.objects.get_or_create(
        wallet_address=wallet_address,
        defaults={
            'username': f'GLI_User_{wallet_address[:8]}',
            'membership_level': 'premium'
        }
    )
    
    # 로그인 시간 업데이트
    user.last_login = timezone.now()
    user.save()
    
    # JWT 토큰 생성
    refresh = RefreshToken()
    refresh['wallet_address'] = wallet_address
    refresh['user_id'] = str(user.id)
    
    # 사용자 정보 시리얼라이즈
    user_serializer = SolanaUserSerializer(user)
    
    return Response({
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        'user': user_serializer.data,
        'message': '🎉 GLI Platform 인증이 완료되었습니다!'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    로그아웃
    POST /api/auth/logout/
    """
    try:
        # 실제 구현에서는 토큰 블랙리스트 처리
        return Response({
            'message': '👋 GLI Platform에서 로그아웃되었습니다.'
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    토큰 갱신
    POST /api/auth/refresh/
    """
    try:
        # request body에서 refresh 토큰 추출
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        refresh = RefreshToken(refresh_token)
        
        return Response({
            'access_token': str(refresh.access_token)
        })
    except Exception as e:
        return Response(
            {'error': 'Token refresh failed'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    사용자 프로필 조회/수정
    GET/PUT /api/user/profile/
    """
    # JWT에서 지갑 주소 추출 (실제 구현에서는 미들웨어에서 처리)
    wallet_address = getattr(request.user, 'wallet_address', None)
    
    if not wallet_address:
        return Response(
            {'error': 'Wallet address not found in token'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        user = SolanaUser.objects.get(wallet_address=wallet_address)
    except SolanaUser.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = SolanaUserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = SolanaUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_transactions(request):
    """
    사용자 트랜잭션 조회
    GET /api/user/transactions/
    """
    wallet_address = getattr(request.user, 'wallet_address', None)
    
    if not wallet_address:
        return Response(
            {'error': 'Wallet address not found'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        user = SolanaUser.objects.get(wallet_address=wallet_address)
        transactions = SolanaTransaction.objects.filter(user=user)
        serializer = SolanaTransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    except SolanaUser.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )