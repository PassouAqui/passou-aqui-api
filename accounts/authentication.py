from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions

class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        
        # Primeiro tenta pegar o token do cookie
        raw_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE')) or None
        
        if raw_token is None and header:
            # Se não encontrou no cookie, tenta do header
            raw_token = self.get_raw_token(header)
            
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        if settings.DEBUG:
            # Em desenvolvimento, não enforçamos CSRF
            return self.get_user(validated_token), validated_token
        else:
            # Em produção, verificamos o CSRF
            self.enforce_csrf(request)
            return self.get_user(validated_token), validated_token

    def enforce_csrf(self, request):
        check = CSRFCheck()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f'CSRF Failed: {reason}') 