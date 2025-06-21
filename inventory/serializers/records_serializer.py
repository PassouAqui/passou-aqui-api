from rest_framework import serializers
from inventory.models import Drug, Records

class RecordsSerializer(serializers.ModelSerializer):
    tag_uid_input = serializers.CharField(max_length=64, write_only=True, required=False)
    arduino = serializers.CharField(max_length=50, required=False)
    
    tag_uid = serializers.CharField(source='drug.tag_uid', read_only=True)
    drug_name = serializers.CharField(source='drug.nome', read_only=True)
    
    class Meta:
        model = Records
        fields = ['id', 'tag_uid_input', 'tag_uid', 'drug_name', 'arduino', 'create_at']
        read_only_fields = ['id', 'create_at']
    
    def validate_tag_uid_input(self, value):
        try:
            Drug.objects.get(tag_uid=value, ativo=True)
        except Drug.DoesNotExist:
            raise serializers.ValidationError("Tag não encontrada")
        return value
    
    def create(self, validated_data):
        tag_uid = validated_data.pop('tag_uid_input', None)
        if tag_uid:
            drug = Drug.objects.get(tag_uid=tag_uid, ativo=True)
            validated_data['drug'] = drug
        
        return super().create(validated_data)
    
class RecordsCreateSerializer(serializers.Serializer):
    tag_uid = serializers.CharField(max_length=64)
    arduino = serializers.CharField(max_length=50, required=False, default='')
    
    def validate_tag_uid(self, value):
        try:
            Drug.objects.get(tag_uid=value, ativo=True)
        except Drug.DoesNotExist:
            raise serializers.ValidationError("Tag não encontrada")
        return value
    
    def create(self, validated_data):
        tag_uid = validated_data['tag_uid']
        arduino = validated_data.get('arduino', '')
        
        drug = Drug.objects.get(tag_uid=tag_uid, ativo=True)
        
        return Records.objects.create(
            drug=drug,
            arduino=arduino
        )