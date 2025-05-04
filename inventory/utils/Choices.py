from django.db import models
from django.utils.translation import gettext_lazy as _

class TarjaChoices(models.TextChoices):
    SEM_TARJA = 'ST', _('Sem Tarja')
<<<<<<< HEAD
    
from django.db import models
from django.utils.translation import gettext_lazy as _

class TarjaChoices(models.TextChoices):
    SEM_TARJA = 'ST', _('Sem Tarja')
=======
>>>>>>> fe6b847 (feat: adicionar campo 'id' ao serializer Drug e incluir opções de tarja no Choices)
    TARJA_AMARELA = 'TA', _('Tarja Amarela')
    TARJA_VERMELHA = 'TV', _('Tarja Vermelha')
    TARJA_PRETA = 'TP', _('Tarja Preta')