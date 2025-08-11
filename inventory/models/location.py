from django_softdelete.models import SoftDeleteModel
from django.db import models
from inventory.models import (Drug)
import uuid

class Location(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medicamento = models.ForeignKey(Drug, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    local = models.CharField(max_length=100)
    origem_arduino = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.lote}"