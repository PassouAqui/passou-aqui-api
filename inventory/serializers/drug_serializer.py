from rest_framework import serializers
from inventory.models import Drug

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['nome', 'descricao', 'tag_uid', 'lote', 'validade', 'ativo', 'tarja']

