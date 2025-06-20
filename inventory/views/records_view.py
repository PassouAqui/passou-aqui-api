from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from inventory.models import Drug, Records
from inventory.serializers import RecordsSerializer
from django.shortcuts import get_object_or_404

import logging

logger = logging.getLogger(__name__)

class RecordsViewSet(viewsets.GenericViewSet):
    queryset = Records.objects.all()
    serializer_class = RecordsSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        logger.info(f"📡 Leitura RFID recebida: {request.data}")
        
        serializer = RecordsSerializer(data=request.data)

        
        if serializer.is_valid():
            tag_uid = serializer.validated_data['tag_uid']
            arduino = serializer.validated_data.get('arduino', '')
            
            try:
                drug = get_object_or_404(Drug, tag_uid=tag_uid, ativo=True)
                
                # Criar a leitura
                reading = Records.objects.create(
                    drug=drug,
                    arduino=arduino
                )
                
                logger.info(f"✅ Leitura registrada: {drug.nome} - {arduino}")
                
                return Response({
                    'success': True,
                    'drug_name': drug.nome,
                    'create_at': reading.create_at
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