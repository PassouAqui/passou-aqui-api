from django.contrib import admin 
from django.urls import path, include 
from accounts.views.token_views import CookieTokenObtainPairView, CookieTokenRefreshView, LogoutView
from accounts.views.profile_view import ProfileView

urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/inventory/', include('inventory.urls')),
    path('api/v1/accounts/', include('accounts.urls')),

    # Endpoints de autenticação
    path('api/v1/auth/login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('api/v1/auth/profile/', ProfileView.as_view(), name='auth-profile'),
    
]