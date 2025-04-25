from rest_framework import viewsets
from inventory.models import Location
from inventory.serializers import LocationSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer