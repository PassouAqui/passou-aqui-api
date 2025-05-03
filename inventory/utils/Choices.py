from django.db import models
from django.utils.translation import gettext_lazy as _

class TarjaChoices(models.TextChoices):
    SEM_TARJA = 'ST', _('Sem Tarja')
    