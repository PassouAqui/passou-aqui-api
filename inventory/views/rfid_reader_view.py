from rest_framework import viewsets
from inventory.models import RFIDReader
from inventory.serializers import RFIDReaderSerializer

class RFIDReaderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows RFID Readers to be viewed or edited.
    """
    queryset = RFIDReader.objects.all()
    serializer_class = RFIDReaderSerializer
