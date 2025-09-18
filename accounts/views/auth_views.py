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
        token = request.data.get('token')
        
        if not token:
            return Response(
                {'error': 'Token não fornecido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verifica o token no Firebase
        firebase_user = firebase_service.verify_token(token)
        
        if not firebase_user:
            return Response(
                {'error': 'Token inválido'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            with transaction.atomic():
                # Busca ou cria o usuário no banco de dados
                user, created = User.objects.get_or_create(
                    firebase_uid=firebase_user['uid'],
                    defaults={
                        'email': firebase_user['email'],
                        'name': firebase_user.get('display_name', ''),
                        'is_verified': firebase_user['email_verified'],
                        'role': 'user' if created else user.role  # Mantém o role existente se o usuário já existe
                    }
                )

                # Atualiza informações do usuário se necessário
                if not created:
                    user.email = firebase_user['email']
                    user.name = firebase_user.get('display_name', user.name)
                    user.is_verified = firebase_user['email_verified']
                    user.save()

                return Response({
                    'success': True,
                    'user_id': user.id,
                    'role': user.role,
                    'is_verified': user.is_verified
                })

        except Exception as e:
            return Response(
                {'error': f'Erro ao processar usuário: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 