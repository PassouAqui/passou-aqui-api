import uuid

from django.db import models
from softdelete.models import SoftDeleteObject

from .location import Location


class RFIDReader(SoftDeleteObject):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)  # Assuming EUI-48 format
    serial_number = models.CharField(max_length=255, blank=True, null=True, unique=True)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, blank=True, null=True, related_name="rfid_readers"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "RFID Reader"
        verbose_name_plural = "RFID Readers"
        ordering = ["name"]
