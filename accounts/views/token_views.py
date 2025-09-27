from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.conf import settings

class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('access'):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                'access_token',
                response.data['access'],
                max_age=cookie_max_age,
                httponly=True,
                samesite='Lax',
                secure=not settings.DEBUG  # True in production
            )
            response.set_cookie(
                'refresh_token',
                response.data['refresh'],
                max_age=cookie_max_age,
                httponly=True,
                samesite='Lax',
                secure=not settings.DEBUG  # True in production
            )
            
            # Remove tokens from response body
            del response.data['access']
            del response.data['refresh']
        
        return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if refresh_token:
            request.data['refresh'] = refresh_token
        
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            response.set_cookie(
                'access_token',
                response.data['access'],
                max_age=3600 * 24 * 14,
                httponly=True,
                samesite='Lax',
                secure=not settings.DEBUG
            )
            
            # Remove token from response body
            del response.data['access']
            
        return response

class LogoutView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response 