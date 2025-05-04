from rest_framework import serializers
from inventory.models import Drug
from inventory.utils.Choices import TarjaChoices
import logging

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
<<<<<<< HEAD
        fields = '__all__'
=======
        fields = ['id','nome', 'descricao', 'tag_uid', 'lote', 'validade', 'ativo', 'tarja']
>>>>>>> fe6b847 (feat: adicionar campo 'id' ao serializer Drug e incluir opções de tarja no Choices)

