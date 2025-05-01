from rest_framework import viewsets
from inventory.models import Drug
from inventory.serializers import DrugSerializer

class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer

