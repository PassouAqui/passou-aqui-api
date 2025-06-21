from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from inventory.models import Drug, Records
from inventory.serializers import RecordsSerializer, RecordsCreateSerializer
from django.shortcuts import get_object_or_404

import logging

logger = logging.getLogger(__name__)

class RecordsViewSet(viewsets.GenericViewSet):
    queryset = Records.objects.all()
    serializer_class = RecordsSerializer
    
    def get_serializer_class(self):
        if self.action == 'register':
            return RecordsCreateSerializer
        return RecordsSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        logger.info(f"📡 Leitura RFID recebida: {request.data}")
        
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            try:
                reading = serializer.save()
                
                logger.info(f"✅ Leitura registrada: {reading.drug.nome} - {reading.arduino}")
                
                return Response({
                    'success': True,
                    'drug_name': reading.drug.nome,
                    'create_at': reading.create_at,
                    'id': reading.id
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"❌ Erro ao registrar leitura: {str(e)}")
                return Response({
                    'success': False,
                    'message': 'Erro interno do servidor'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)