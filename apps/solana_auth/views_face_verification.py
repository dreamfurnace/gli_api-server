"""
얼굴 인증 관련 API 뷰
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime

from .models import SolanaUser, FaceVerification
from .serializers import (
    FaceVerificationCreateSerializer,
    FaceVerificationSerializer
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_face_verification(request, user_id):
    """
    얼굴 인증 결과 제출
    POST /api/users/{user_id}/face-verification/
    """
    # 사용자 존재 확인
    user = get_object_or_404(SolanaUser, id=user_id)

    # 요청한 사용자가 본인인지 확인 (또는 관리자)
    if str(request.user.id) != str(user_id) and not request.user.is_staff:
        return Response(
            {'error': '본인의 얼굴 인증 결과만 제출할 수 있습니다.'},
            status=status.HTTP_403_FORBIDDEN
        )

    # 데이터 검증
    serializer = FaceVerificationCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                'error': '유효하지 않은 데이터입니다.',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    validated_data = serializer.validated_data

    # FaceVerification 인스턴스 생성
    face_verification = FaceVerification.objects.create(
        user=user,
        verified=validated_data['verified'],
        confidence=validated_data['confidence'],
        liveness_score=validated_data['liveness_score'],
        attempts=validated_data.get('attempts', 1),
        check_details=validated_data.get('check_details'),
        verification_timestamp=validated_data['timestamp']
    )

    # 생성된 인스턴스 시리얼라이즈
    response_serializer = FaceVerificationSerializer(face_verification)

    return Response(
        {
            'success': True,
            'message': '✅ 얼굴 인증 결과가 성공적으로 저장되었습니다.',
            'data': response_serializer.data
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_face_verification_status(request, user_id):
    """
    최신 얼굴 인증 상태 조회
    GET /api/users/{user_id}/face-verification/status/
    """
    # 사용자 존재 확인
    user = get_object_or_404(SolanaUser, id=user_id)

    # 권한 확인
    if str(request.user.id) != str(user_id) and not request.user.is_staff:
        return Response(
            {'error': '본인의 얼굴 인증 상태만 조회할 수 있습니다.'},
            status=status.HTTP_403_FORBIDDEN
        )

    # 가장 최근의 인증 기록 조회
    latest_verification = FaceVerification.objects.filter(
        user=user
    ).order_by('-created_at').first()

    if not latest_verification:
        return Response(
            {
                'hasVerification': False,
                'message': '얼굴 인증 기록이 없습니다.'
            },
            status=status.HTTP_200_OK
        )

    serializer = FaceVerificationSerializer(latest_verification)

    return Response(
        {
            'hasVerification': True,
            'data': serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_face_verification_history(request, user_id):
    """
    얼굴 인증 히스토리 조회
    GET /api/users/{user_id}/face-verification/history/
    """
    # 사용자 존재 확인
    user = get_object_or_404(SolanaUser, id=user_id)

    # 권한 확인
    if str(request.user.id) != str(user_id) and not request.user.is_staff:
        return Response(
            {'error': '본인의 얼굴 인증 히스토리만 조회할 수 있습니다.'},
            status=status.HTTP_403_FORBIDDEN
        )

    # 페이지네이션 파라미터
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))

    # 필터링 파라미터
    verified_filter = request.GET.get('verified')  # 'true', 'false', None

    # 기본 쿼리셋
    queryset = FaceVerification.objects.filter(user=user)

    # 필터 적용
    if verified_filter is not None:
        if verified_filter.lower() == 'true':
            queryset = queryset.filter(verified=True)
        elif verified_filter.lower() == 'false':
            queryset = queryset.filter(verified=False)

    # 정렬 (최신순)
    queryset = queryset.order_by('-created_at')

    # 페이지네이션
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    total_count = queryset.count()
    verifications = queryset[start_idx:end_idx]

    # 시리얼라이즈
    serializer = FaceVerificationSerializer(verifications, many=True)

    return Response(
        {
            'total': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size,
            'data': serializer.data
        },
        status=status.HTTP_200_OK
    )
