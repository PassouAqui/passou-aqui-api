from django.db import models
from django.utils.translation import gettext_lazy as _

class TarjaChoices(models.TextChoices):
    SEM_TARJA = 'ST', _('Sem Tarja')
    TARJA_AMARELA = 'TA', _('Tarja Amarela')
    TARJA_VERMELHA = 'TV', _('Tarja Vermelha')
    TARJA_PRETA = 'TP', _('Tarja Preta')