from rest_framework.views import APIView
from rest_framework.response import Response
<<<<<<< HEAD
from rest_framework import permissions, status
from django.contrib.auth.models import User
from django.db import transaction
import logging

from accounts.serializers import UserRegistrationSerializer

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'error': 'Dados inválidos',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                user = serializer.save()
                logger.info(f"Usuário {user.username} criado com sucesso")
                
                return Response(
                    {
                        'success': 'Usuário criado com sucesso!',
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'first_name': user.first_name,
                            'last_name': user.last_name
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
                
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {str(e)}")
            return Response(
                {'error': 'Erro interno do servidor. Tente novamente mais tarde.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
=======
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import RegisterSerializer, UserSerializer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        # gera os tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # serializa o usuário (sem expor senha)
        user_data = UserSerializer(user).data

        return Response({
            'user':    user_data,
            'refresh': str(refresh),
            'access':  str(access),
        }, status=status.HTTP_201_CREATED)
>>>>>>> 68b3b0d (feat: aprimorar registro de usuário com geração de tokens JWT)
