import firebase_admin
from firebase_admin import auth, credentials
from django.conf import settings
from typing import Dict, Optional

class FirebaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            # Inicializa o Firebase Admin SDK apenas uma vez
            try:
                firebase_admin.get_app()
            except ValueError:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
                firebase_admin.initialize_app(cred)
        return cls._instance

    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verifica o token do Firebase e retorna os dados do usuário
        """
        try:
            # Verifica o token
            decoded_token = auth.verify_id_token(token)
            
            # Obtém o usuário do Firebase
            user = auth.get_user(decoded_token['uid'])
            
            # Retorna os dados necessários
            return {
                'uid': user.uid,
                'email': user.email,
                'email_verified': user.email_verified,
                'display_name': user.display_name,
                'photo_url': user.photo_url,
            }
        except Exception as e:
            print(f"Erro ao verificar token: {str(e)}")
            return None

firebase_service = FirebaseService() 