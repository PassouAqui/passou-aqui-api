import uuid
from django.utils import timezone
from django_softdelete.models import SoftDeleteModel
from django.db import models
from inventory.models import Drug

class Records(SoftDeleteModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drug = models.ForeignKey(
        Drug,
        on_delete=models.CASCADE,
        related_name='records'
    )
    arduino = models.CharField(max_length=50, blank=True)
    create_at =  models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id}" 