from django.db import models
from django_softdelete.models import SoftDeleteModel
from .cart import Cart
from .drug import Drug

class CartItem(SoftDeleteModel):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.drug.nome}" 