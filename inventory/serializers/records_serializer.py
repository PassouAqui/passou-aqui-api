from rest_framework import serializers
from inventory.models import Drug, Records

class RecordsSerializer(serializers.Serializer):
    tag_uid = serializers.CharField(max_length=64)
    arduino_id = serializers.CharField(max_length=50, required=False, default='')
    
    def validate_tag_uid(self, value):
        try:
            Drug.objects.get(tag_uid=value, ativo=True)
        except Drug.DoesNotExist:
            raise serializers.ValidationError("Tag não encontrada")
        return value
    
    class Meta:
        model = Records