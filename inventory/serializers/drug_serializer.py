from rest_framework import serializers
from inventory.models import Drug
from inventory.utils.Choices import TarjaChoices
import logging

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['id', 'nome', 'descricao', 'tag_uid', 'lote', 'validade', 'ativo', 'tarja']
        read_only_fields = ['id']

    def validate_validade(self, value):
        """Validate that the expiration date is not in the past"""
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("A data de validade não pode ser no passado")
        return value

    def validate_tarja(self, value):
        """Validate that the tarja value is valid"""
        logger = logging.getLogger(__name__)
        logger.info(f"Validando tarja: {value}")
        logger.info(f"TarjaChoices disponíveis: {dict(TarjaChoices)}")
        logger.info(f"TarjaChoices valores: {[choice.value for choice in TarjaChoices]}")
        
        if value not in [choice.value for choice in TarjaChoices]:
            logger.error(f"Tarja inválida: {value}")
            raise serializers.ValidationError("Tarja inválida")
        return value

    def validate_tag_uid(self, value):
        """Validate that the tag_uid is unique if provided"""
        if value:
            if Drug.objects.filter(tag_uid=value).exclude(id=self.instance.id if self.instance else None).exists():
                raise serializers.ValidationError("Esta tag RFID já está em uso")
        return value

