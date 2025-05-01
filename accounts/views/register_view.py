from rest_framework.views import APIView
from rest_framework.response import Response
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
