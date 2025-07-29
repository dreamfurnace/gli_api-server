# apps/common/views.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """GLI API 서버 상태 확인"""
    return Response({
        'status': 'ok',
        'message': 'GLI API Server is running'
    }, status=status.HTTP_200_OK)