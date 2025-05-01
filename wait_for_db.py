import os
import time
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediTrack.settings")

print("⏳ Aguardando o banco de dados...")

while True:
    try:
        connections['default'].cursor()
        break
    except OperationalError:
        print("🔁 Banco ainda não disponível, aguardando...")
        time.sleep(1)

print("✅ Banco disponível!")
