from firebase_admin import auth
from firebase_admin import credentials

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from ..serializers.auth_serializer import LoginSerializer, UserSerializer
from rest_framework.views import APIView
from ..services.firebase_service import firebase_service
from ..models import User
from django.db import transaction
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class LoginView(generics.GenericAPIView):
    """
    View for handling user login and token generation.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data['email'])
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class RefreshTokenView(generics.GenericAPIView):
    """
    View for refreshing JWT tokens.
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            return Response({
                'access': str(token.access_token),
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Invalid refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )

class VerifyTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("🔍 VerifyTokenView: Iniciando verificação de token")
        
        token = request.data.get('token')
        if not token:
            logger.error("🔍 VerifyTokenView: Token não fornecido")
            return Response(
                {'error': 'Token não fornecido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"🔍 VerifyTokenView: Token recebido (primeiros 20 chars): {token[:20]}...")

        firebase_user = None 
        try:
            logger.info("🔍 VerifyTokenView: Tentando verificar token no Firebase...")
            firebase_user = auth.verify_id_token(token)
            logger.info(f"🔍 VerifyTokenView: Token verificado com sucesso. UID: {firebase_user.get('uid')}")
        except Exception as e:
            logger.error(f"🔍 VerifyTokenView: Erro ao verificar token no Firebase: {str(e)}")
            return Response(
                {'error': f'Token inválido ou expirado: {str(e)}'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            logger.info("🔍 VerifyTokenView: Iniciando transação no banco de dados...")
            with transaction.atomic():
                user, created = User.objects.get_or_create(
                    firebase_uid=firebase_user['uid'],
                    defaults={
                        'username': firebase_user['email'],
                        'email': firebase_user['email'],
                        'name': firebase_user.get('display_name', ''),
                        'is_verified': firebase_user['email_verified'],
                        'role': 'user',
                    }
                )

                if not created:
                    logger.info(f"🔍 VerifyTokenView: Usuário existente encontrado: {user.email}")
                    user.email = firebase_user['email']
                    user.name = firebase_user.get('display_name', user.name)
                    user.is_verified = firebase_user['email_verified']
                    user.save()
                else:
                    logger.info(f"🔍 VerifyTokenView: Novo usuário criado: {user.email}")

                response_data = {
                    'success': True,
                    'user_id': user.id,
                    'role': user.role,
                    'is_verified': user.is_verified,
                    'firebase_uid': firebase_user['uid']
                }
                
                logger.info(f"🔍 VerifyTokenView: Resposta de sucesso: {response_data}")
                return Response(response_data)

        except Exception as e:
            logger.error(f"🔍 VerifyTokenView: Erro ao processar usuário no DB: {str(e)}")
            return Response(
                {'error': f'Erro ao processar usuário no DB: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )