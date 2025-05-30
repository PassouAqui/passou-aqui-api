from rest_framework import serializers
from inventory.models import RFIDReader # Consistent import path

class RFIDReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFIDReader
        fields = '__all__'
