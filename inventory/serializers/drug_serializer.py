from rest_framework import serializers
from inventory.models import Drug
from inventory.utils.Choices import TarjaChoices
import logging

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'

