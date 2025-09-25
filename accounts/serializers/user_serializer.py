from rest_framework import serializers
from django.contrib.auth.models import User
import logging
import re

logger = logging.getLogger(__name__)


class UserRegistrationSerializer(serializers.ModelSerializer):    
    re_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 're_password')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True}
        }
    
    def validate_username(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Nome de usuário deve ter pelo menos 3 caracteres.")
        
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value
    
    def validate_password(self, value):
        errors = []
        
        if len(value) < 8:
            errors.append("A senha deve ter pelo menos 8 caracteres.")
        
        if not re.search(r'[A-Za-z]', value):
            errors.append("A senha deve conter pelo menos uma letra.")
        
        if not re.search(r'\d', value):
            errors.append("A senha deve conter pelo menos um número.")
        
        common_passwords = ['12345678', 'password', '123456789', 'qwerty', 'abc123']
        if value.lower() in common_passwords:
            errors.append("Esta senha é muito comum.")
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({
                're_password': "As senhas não coincidem."
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('re_password', None)
        return User.objects.create_user(**validated_data)