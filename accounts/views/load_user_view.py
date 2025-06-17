from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer

class LoadUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        try:
            user = request.user
            
            if not user.is_authenticated:
                return Response(
                    {'error': 'User not authenticated'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            user_serializer = UserSerializer(user)
            return Response(
                {
                    'username': user_serializer.data['username'],
                    'first_name' : user_serializer.data['first_name'],
                    'last_name' : user_serializer.data['last_name']
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': 'Something went wrong when trying to load user'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )