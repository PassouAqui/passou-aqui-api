from django.db import models
from .drug import Drug
from .location import Location

class Inventory(models.Model):
    """
    Modelo para controlar o inventário de medicamentos em diferentes localizações.
    """
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='inventory_items')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='inventory_items')
    quantity = models.PositiveIntegerField(default=0)
    expiration_date = models.DateField(null=True, blank=True)
    movement_type = models.CharField(
        max_length=20,
        choices=[
            ('ENTRY', 'Entrada'),
            ('EXIT', 'Saída'),
            ('ADJUSTMENT', 'Ajuste'),
        ],
        default='ENTRY'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Inventário'
        verbose_name_plural = 'Inventários'
        unique_together = ['drug', 'location']
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.drug.name} - {self.location.name} ({self.quantity})" 