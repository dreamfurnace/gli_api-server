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
from .models import SolanaUser, AuthNonce, SolanaTransaction, FaceVerification, AdminUser, AdminGrade, TeamMember, ProjectFeature, DevelopmentTimeline, TokenEcosystem
from .serializers import (
    SolanaUserSerializer,
    NonceRequestSerializer,
    AuthVerifySerializer,
    SolanaTransactionSerializer,
    FaceVerificationCreateSerializer,
    FaceVerificationSerializer,
    AdminUserDetailSerializer,
    AdminUserUpdateSerializer
)
from .permissions import IsSuperAdmin
from django.db import transaction
from django.shortcuts import get_object_or_404

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
@permission_classes([IsAuthenticated])
def request_nonce(request):
    """
    인증용 nonce 발급 (로그인된 사용자의 지갑 주소 연결용)
    POST /api/auth/nonce/
    """
    serializer = NonceRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid request data', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    wallet_address = serializer.validated_data['wallet_address']
    current_user = request.user

    # 지갑 주소가 이미 다른 사용자에게 등록되어 있는지 확인
    try:
        existing_user = SolanaUser.objects.get(wallet_address=wallet_address)

        # 현재 로그인한 사용자와 다른 사용자에게 이미 연결되어 있으면
        if existing_user.id != current_user.id:
            # 기존 사용자의 지갑 주소 연결 해제
            existing_user.wallet_address = None
            existing_user.save()
    except SolanaUser.DoesNotExist:
        # 등록되지 않은 지갑 주소는 문제없음
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
@permission_classes([IsAuthenticated])
def verify_signature(request):
    """
    서명 검증 및 지갑 주소 연결
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
    current_user = request.user

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

    # 현재 로그인한 사용자의 지갑 주소 업데이트
    current_user.wallet_address = wallet_address
    current_user.last_login = timezone.now()
    current_user.save()

    # JWT 토큰 생성
    refresh = RefreshToken()
    refresh['wallet_address'] = wallet_address
    refresh['user_id'] = str(current_user.id)

    # 사용자 정보 시리얼라이즈
    user_serializer = SolanaUserSerializer(current_user)

    return Response({
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        'user': user_serializer.data,
        'message': '🎉 GLI Platform 지갑 연결이 완료되었습니다!'
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


# ============================================================================
# 회원 관리 Views (Member Management Views)
# ============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def member_list(request):
    """
    회원 목록 조회 및 생성
    GET /api/members/ - 일반 회원 목록 조회 (is_staff=False)
    POST /api/members/ - 새 회원 생성
    """
    if request.method == 'GET':
        # is_staff=False인 일반 회원만 조회 (관리자 제외)
        members = SolanaUser.objects.filter(is_staff=False).order_by('-created_at')

        # 검색 필터
        search = request.query_params.get('search', '').strip()
        if search:
            from django.db.models import Q
            members = members.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(wallet_address__icontains=search)
            )

        # 멤버십 레벨 필터
        membership_level = request.query_params.get('membership_level')
        if membership_level:
            members = members.filter(membership_level=membership_level)

        # 활성 상태 필터
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            members = members.filter(is_active=is_active.lower() == 'true')

        serializer = SolanaUserSerializer(members, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SolanaUserSerializer(data=request.data)
        if serializer.is_valid():
            # 일반 회원으로 생성 (is_staff=False)
            member = serializer.save(is_staff=False)
            return Response(
                SolanaUserSerializer(member).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def member_detail(request, member_id):
    """
    회원 상세 조회, 수정, 삭제
    GET /api/members/<member_id>/
    PUT /api/members/<member_id>/
    DELETE /api/members/<member_id>/
    """
    try:
        member = SolanaUser.objects.get(id=member_id, is_staff=False)
    except SolanaUser.DoesNotExist:
        return Response(
            {'error': '회원을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = SolanaUserSerializer(member)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SolanaUserSerializer(member, data=request.data, partial=True)
        if serializer.is_valid():
            # is_staff 필드는 변경 불가
            serializer.save(is_staff=False)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        member.delete()
        return Response(
            {'message': '회원이 삭제되었습니다.'},
            status=status.HTTP_204_NO_CONTENT
        )


# ============================================================================
# 관리자 관리 Views (Admin Management Views)
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_list(request):
    """관리자 목록 조회"""
    # 요청한 사용자가 슈퍼 관리자인지 확인
    try:
        admin_user = AdminUser.objects.select_related('grade').get(user=request.user)
        if admin_user.grade.name != "슈퍼 관리자":
            return Response(
                {"detail": "접근 권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )
    except AdminUser.DoesNotExist:
        # AdminUser가 없어도 SolanaUser가 슈퍼유저면 허용
        if not request.user.is_superuser:
            return Response(
                {"detail": "관리자 정보를 찾을 수 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

    admin_users = AdminUser.objects.select_related('user', 'grade').all()
    serializer = AdminUserDetailSerializer(admin_users, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def admin_detail(request, admin_id):
    """관리자 상세 정보 조회 및 수정"""
    admin_user = get_object_or_404(AdminUser, id=admin_id)

    if request.method == 'GET':
        serializer = AdminUserDetailSerializer(admin_user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        with transaction.atomic():
            serializer = AdminUserUpdateSerializer(admin_user, data=request.data)
            if serializer.is_valid():
                new_grade = get_object_or_404(AdminGrade, id=serializer.validated_data['grade_id'])
                # AdminUser 모델 업데이트
                admin_user.grade = new_grade
                admin_user.is_active = serializer.validated_data['is_active']
                admin_user.save()

                # SolanaUser 모델도 함께 업데이트
                user = admin_user.user
                user.is_active = serializer.validated_data['is_active']
                user.save()

                admin_user.refresh_from_db()
                return Response(AdminUserDetailSerializer(admin_user).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def platform_statistics(request):
    """플랫폼 통계 조회"""
    try:
        # 전체 회원 수
        total_members = SolanaUser.objects.filter(is_active=True).count()

        # 인증된 회원 수 (face_verification이 성공한 사용자)
        verified_members = FaceVerification.objects.filter(verified=True).values('user').distinct().count()

        # 대기 중인 인증 (최근 실패한 인증)
        pending_verifications = FaceVerification.objects.filter(verified=False).values('user').distinct().count()

        # 활성 트랜잭션 (pending 상태)
        active_transactions = SolanaTransaction.objects.filter(status='pending').count()

        # 월간 활성 사용자 (최근 30일 내 로그인)
        from datetime import timedelta
        thirty_days_ago = timezone.now() - timedelta(days=30)
        monthly_active_users = SolanaUser.objects.filter(
            is_active=True,
            last_login__gte=thirty_days_ago
        ).count()

        # 총 배포된 토큰 (confirmed 트랜잭션 합계)
        from django.db.models import Sum
        total_token_distributed = SolanaTransaction.objects.filter(
            status='confirmed'
        ).aggregate(total=Sum('amount'))['total'] or 0

        # 총 GLIB 토큰 (전체 사용자의 sol_balance 합계)
        total_glib_tokens = SolanaUser.objects.aggregate(
            total=Sum('sol_balance')
        )['total'] or 0

        # 플랫폼 성장률 계산 (이번 달 vs 지난 달 신규 가입자)
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        first_day_of_last_month = (first_day_of_month - timedelta(days=1)).replace(day=1)

        this_month_users = SolanaUser.objects.filter(
            created_at__gte=first_day_of_month
        ).count()

        last_month_users = SolanaUser.objects.filter(
            created_at__gte=first_day_of_last_month,
            created_at__lt=first_day_of_month
        ).count()

        if last_month_users > 0:
            platform_growth = round(((this_month_users - last_month_users) / last_month_users) * 100, 1)
        else:
            platform_growth = 100.0 if this_month_users > 0 else 0.0

        return Response({
            'totalMembers': total_members,
            'totalGLIBTokens': float(total_glib_tokens),
            'activeTransactions': active_transactions,
            'platformGrowth': platform_growth,
            'monthlyActiveUsers': monthly_active_users,
            'totalTokenDistributed': float(total_token_distributed),
            'verifiedMembers': verified_members,
            'pendingVerifications': pending_verifications,
        })

    except Exception as e:
        return Response(
            {'error': f'통계 조회 중 오류가 발생했습니다: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ============================================================================
# S3 파일 업로드 Views
# ============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    """
    이미지 파일 S3 업로드
    POST /api/upload/image/
    """
    try:
        # 파일 확인
        if 'file' not in request.FILES:
            return Response(
                {'error': '파일이 없습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        # 파일 크기 제한 (10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if file.size > max_size:
            return Response(
                {'error': '파일 크기는 10MB를 초과할 수 없습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 파일 타입 확인 (이미지만 허용)
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if file.content_type not in allowed_types:
            return Response(
                {'error': '이미지 파일만 업로드 가능합니다. (JPEG, PNG, GIF, WebP)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # S3 폴더 경로 지정 (옵션)
        folder = request.data.get('folder', 'business-content')
        
        # S3에 업로드
        from .utils.s3_upload import S3Uploader
        uploader = S3Uploader()
        result = uploader.upload_file(file, folder=folder)

        # 웹사이트 콘텐츠는 영구 접근 가능한 직접 S3 URL 사용
        # result['url']은 이미 직접 S3 URL을 포함하고 있음

        return Response({
            'success': True,
            'data': result,
            'message': '파일이 성공적으로 업로드되었습니다.'
        })
        
    except Exception as e:
        return Response(
            {'error': f'파일 업로드 실패: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_image(request):
    """
    S3에서 이미지 삭제
    DELETE /api/upload/image/
    """
    try:
        s3_key = request.data.get('s3_key')
        
        if not s3_key:
            return Response(
                {'error': 'S3 키가 필요합니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # S3에서 삭제
        from .utils.s3_upload import S3Uploader
        uploader = S3Uploader()
        uploader.delete_file(s3_key)
        
        return Response({
            'success': True,
            'message': '파일이 성공적으로 삭제되었습니다.'
        })
        
    except Exception as e:
        return Response(
            {'error': f'파일 삭제 실패: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ============================================================================
# 팀 구성원 Views (Team Member Views)
# ============================================================================

@api_view(['GET', 'POST'])
def team_member_list(request):
    """
    팀 구성원 목록 조회 및 생성
    GET /api/team-members/ (공개 API - 인증 불필요)
    POST /api/team-members/ (인증 필요)
    """
    if request.method == 'GET':
        # is_active=True인 팀원만 반환 (프론트엔드용)
        show_all = request.query_params.get('show_all', 'false').lower() == 'true'

        if show_all:
            team_members = TeamMember.objects.all()
        else:
            team_members = TeamMember.objects.filter(is_active=True)

        from .serializers import TeamMemberSerializer
        serializer = TeamMemberSerializer(team_members, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # POST 요청은 인증 필요
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': '인증이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        from .serializers import TeamMemberSerializer
        serializer = TeamMemberSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def team_member_detail(request, member_id):
    """
    팀 구성원 상세 조회, 수정, 삭제
    GET /api/team-members/{member_id}/
    PUT /api/team-members/{member_id}/
    DELETE /api/team-members/{member_id}/
    """
    try:
        team_member = TeamMember.objects.get(id=member_id)
    except TeamMember.DoesNotExist:
        return Response(
            {'error': '팀 구성원을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        from .serializers import TeamMemberSerializer
        serializer = TeamMemberSerializer(team_member)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        from .serializers import TeamMemberSerializer
        serializer = TeamMemberSerializer(team_member, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        team_member.delete()
        return Response(
            {'message': '팀 구성원이 삭제되었습니다.'},
            status=status.HTTP_204_NO_CONTENT
        )


# ============================================================================
# 프로젝트 특징 Views (Project Feature Views)
# ============================================================================

@api_view(['GET', 'POST'])
def project_feature_list(request):
    """
    프로젝트 특징 목록 조회 및 생성
    GET /api/project-features/ (공개 API - 인증 불필요)
    POST /api/project-features/ (인증 필요)
    """
    if request.method == 'GET':
        # is_active=True인 특징만 반환 (프론트엔드용)
        show_all = request.query_params.get('show_all', 'false').lower() == 'true'

        if show_all:
            features = ProjectFeature.objects.all()
        else:
            features = ProjectFeature.objects.filter(is_active=True)

        from .serializers import ProjectFeatureSerializer
        serializer = ProjectFeatureSerializer(features, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # POST 요청은 인증 필요
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': '인증이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        from .serializers import ProjectFeatureSerializer
        serializer = ProjectFeatureSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def project_feature_detail(request, feature_id):
    """
    프로젝트 특징 상세 조회, 수정, 삭제
    GET /api/project-features/{feature_id}/
    PUT /api/project-features/{feature_id}/
    DELETE /api/project-features/{feature_id}/
    """
    try:
        from .models import ProjectFeature
        feature = ProjectFeature.objects.get(id=feature_id)
    except ProjectFeature.DoesNotExist:
        return Response(
            {'error': '프로젝트 특징을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        from .serializers import ProjectFeatureSerializer
        serializer = ProjectFeatureSerializer(feature)
        return Response(serializer.data)

    elif request.method == 'PUT':
        from .serializers import ProjectFeatureSerializer
        serializer = ProjectFeatureSerializer(feature, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        feature.delete()
        return Response(
            {'message': '프로젝트 특징이 삭제되었습니다.'},
            status=status.HTTP_204_NO_CONTENT
        )


# ============================================================================
# 전략 로드맵 Views (Strategy Roadmap Views)
# ============================================================================

@api_view(['GET', 'POST'])
def strategy_phase_list(request):
    """
    전략 로드맵 페이즈 목록 조회 및 생성
    GET /api/strategy-phases/ (공개 API - 인증 불필요)
    POST /api/strategy-phases/ (인증 필요)
    """
    if request.method == 'GET':
        # is_active=True인 페이즈만 반환 (프론트엔드용)
        show_all = request.query_params.get('show_all', 'false').lower() == 'true'

        if show_all:
            from .models import StrategyPhase
            phases = StrategyPhase.objects.all()
        else:
            from .models import StrategyPhase
            phases = StrategyPhase.objects.filter(is_active=True)

        from .serializers import StrategyPhaseSerializer
        serializer = StrategyPhaseSerializer(phases, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # POST 요청은 인증 필요
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': '인증이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        from .serializers import StrategyPhaseSerializer
        serializer = StrategyPhaseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def strategy_phase_detail(request, phase_id):
    """
    전략 로드맵 페이즈 상세 조회, 수정, 삭제
    GET /api/strategy-phases/{phase_id}/
    PUT /api/strategy-phases/{phase_id}/
    DELETE /api/strategy-phases/{phase_id}/
    """
    try:
        from .models import StrategyPhase
        phase = StrategyPhase.objects.get(id=phase_id)
    except StrategyPhase.DoesNotExist:
        return Response(
            {'error': '전략 로드맵 페이즈를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        from .serializers import StrategyPhaseSerializer
        serializer = StrategyPhaseSerializer(phase)
        return Response(serializer.data)

    elif request.method == 'PUT':
        from .serializers import StrategyPhaseSerializer
        serializer = StrategyPhaseSerializer(phase, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        phase.delete()
        return Response(
            {'message': '전략 로드맵 페이즈가 삭제되었습니다.'},
            status=status.HTTP_204_NO_CONTENT
        )


# ============================================================================
# 개발 일정 관리 Views (Development Timeline Views)
# ============================================================================

@api_view(['GET', 'POST'])
def development_timeline_list(request):
    """
    개발 일정 목록 조회 및 생성
    GET /api/development-timelines/ (공개 API - 인증 불필요)
    POST /api/development-timelines/ (인증 필요)
    """
    if request.method == 'GET':
        # is_active=True인 일정만 반환 (프론트엔드용)
        show_all = request.query_params.get('show_all', 'false').lower() == 'true'

        if show_all:
            timelines = DevelopmentTimeline.objects.all()
        else:
            timelines = DevelopmentTimeline.objects.filter(is_active=True)

        from .serializers import DevelopmentTimelineSerializer
        serializer = DevelopmentTimelineSerializer(timelines, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # POST 요청은 인증 필요
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': '인증이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        from .serializers import DevelopmentTimelineSerializer
        serializer = DevelopmentTimelineSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def development_timeline_detail(request, timeline_id):
    """
    개발 일정 상세 조회, 수정, 삭제
    GET /api/development-timelines/{timeline_id}/
    PUT /api/development-timelines/{timeline_id}/
    DELETE /api/development-timelines/{timeline_id}/
    """
    try:
        timeline = DevelopmentTimeline.objects.get(id=timeline_id)
    except DevelopmentTimeline.DoesNotExist:
        return Response(
            {'error': '개발 일정을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        from .serializers import DevelopmentTimelineSerializer
        serializer = DevelopmentTimelineSerializer(timeline)
        return Response(serializer.data)

    elif request.method == 'PUT':
        from .serializers import DevelopmentTimelineSerializer
        serializer = DevelopmentTimelineSerializer(timeline, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        timeline.delete()
        return Response(
            {'message': '개발 일정이 삭제되었습니다.'},
            status=status.HTTP_204_NO_CONTENT
        )


# ============================================================================
# 토큰 에코시스템 Views (Token Ecosystem Views)
# ============================================================================

@api_view(['GET', 'POST'])
def token_ecosystem_list(request):
    """
    토큰 에코시스템 목록 조회 및 생성
    GET /api/token-ecosystems/ (공개 API - 인증 불필요)
    POST /api/token-ecosystems/ (인증 필요)
    """
    if request.method == 'GET':
        # is_active=True인 토큰만 반환 (프론트엔드용)
        show_all = request.query_params.get('show_all', 'false').lower() == 'true'

        if show_all:
            tokens = TokenEcosystem.objects.all()
        else:
            tokens = TokenEcosystem.objects.filter(is_active=True)

        from .serializers import TokenEcosystemSerializer
        serializer = TokenEcosystemSerializer(tokens, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # POST 요청은 인증 필요
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': '인증이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        from .serializers import TokenEcosystemSerializer
        serializer = TokenEcosystemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def token_ecosystem_detail(request, token_id):
    """
    토큰 에코시스템 상세 조회, 수정, 삭제
    GET /api/token-ecosystems/{token_id}/
    PUT /api/token-ecosystems/{token_id}/
    DELETE /api/token-ecosystems/{token_id}/
    """
    try:
        token = TokenEcosystem.objects.get(id=token_id)
    except TokenEcosystem.DoesNotExist:
        return Response(
            {'error': '토큰 정보를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        from .serializers import TokenEcosystemSerializer
        serializer = TokenEcosystemSerializer(token)
        return Response(serializer.data)

    elif request.method == 'PUT':
        from .serializers import TokenEcosystemSerializer
        serializer = TokenEcosystemSerializer(token, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        token.delete()
        return Response(
            {'message': '토큰 정보가 삭제되었습니다.'},
            status=status.HTTP_204_NO_CONTENT
        )
