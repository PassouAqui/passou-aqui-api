from django.contrib import admin 
from django.urls import path, include 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView 


urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/inventory/', include('inventory.urls')),
    path('api/v1/accounts/', include('accounts.urls')),


    path('api/v1/auth/token', TokenObtainPairView.as_view()),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view()),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view()),

]
