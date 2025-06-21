from django.urls import path
from .views import RegisterView, LoadUserView
from .views.token_views import CookieTokenObtainPairView, CookieTokenRefreshView, LogoutView
from .views.profile_view import ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('user/', LoadUserView.as_view()),
    path('token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('', ProfileView.as_view(), name='user_profile'),  
]
