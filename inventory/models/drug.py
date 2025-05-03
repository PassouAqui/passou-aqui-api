from django_softdelete.models import SoftDeleteModel
from django.db import models
import uuid
from inventory.utils.Choices import TarjaChoices 

class Drug(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    tag_uid = models.CharField(max_length=64, unique=True)  # RFID
    lote = models.CharField(max_length=50)
    validade = models.DateField()
    ativo = models.BooleanField(default=True)
    tarja = models.CharField(choices=TarjaChoices, max_length=2,default=TarjaChoices.SEM_TARJA)

    def __str__(self):
        return f"{self.nome} - {self.lote}"