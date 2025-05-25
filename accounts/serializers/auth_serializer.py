from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login requests.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """
        Validate user credentials.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()
            
            if user and user.check_password(password):
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                return attrs
            else:
                raise serializers.ValidationError('Invalid email or password.')
        else:
            raise serializers.ValidationError('Both email and password are required.')

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user data.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active')
        read_only_fields = ('id', 'is_active') 