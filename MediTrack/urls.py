from django.contrib import admin 
from django.urls import path, include 
from accounts.views.token_views import CookieTokenObtainPairView, CookieTokenRefreshView, LogoutView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/inventory/', include('inventory.urls')),
    path('api/v1/accounts/', include('accounts.urls')),

    # Endpoints de autenticação
    # path('api/v1/auth/login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/auth/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    # path('api/v1/auth/logout/', LogoutView.as_view(), name='auth_logout'),
    # path('api/v1/auth/login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/auth/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    # path('api/v1/auth/logout/', LogoutView.as_view(), name='auth_logout'),


    #simple jwt
    path('api/v1/auth/token/', TokenObtainPairView.as_view()),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view()),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view()),
]
