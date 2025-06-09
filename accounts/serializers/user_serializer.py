from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'name', 'role', 'is_verified', 'phone_number')
        read_only_fields = ('id', 'is_active')