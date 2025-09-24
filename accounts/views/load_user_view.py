from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer
class LoadUserView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)
            return Response(
                {'user' : user.data},
                status=status.HTTP_200_OK
            )

        except:
            return Response({
                'error': 'Erro ao exibir informações do usuário'
            },
            status=status.HTTP_500_SERVER_ERROR
            )