from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from inventory.models import Drug
from inventory.serializers.drug_serializer import DrugSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
import logging
from django.db import models

logger = logging.getLogger(__name__)

class DrugViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing medications (Drugs)
    """
    serializer_class = DrugSerializer
    # permission_classes = [IsAuthenticated]
    queryset = Drug.objects.all()

    def get_queryset(self):
        """
        Filtra os medicamentos por:
        - active: status ativo/inativo
        - search: busca por nome, descrição ou lote
        - tarja: filtro por tipo de tarja
        """
        queryset = Drug.objects.all()
        
        # Filtro por status ativo/inativo
        active = self.request.query_params.get('active', None)
        if active is not None:
            queryset = queryset.filter(ativo=active.lower() == 'true')
        
        # Filtro por busca
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(nome__icontains=search) |
                models.Q(descricao__icontains=search) |
                models.Q(lote__icontains=search)
            )
        
        # Filtro por tarja
        tarja = self.request.query_params.get('tarja', None)
        if tarja:
            queryset = queryset.filter(tarja=tarja)
        
        return queryset.order_by('nome')  # Ordena por nome para melhor usabilidade

    def create(self, request, *args, **kwargs):
        print("1. Iniciando create")
        print(f"2. Dados recebidos: {request.data}")
        try:
            serializer = self.get_serializer(data=request.data)
            print("3. Serializer criado")
            serializer.is_valid(raise_exception=True)
            print("4. Dados validados")
            self.perform_create(serializer)
            print("5. Create realizado")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"❌ Erro no create: {str(e)}")
            if hasattr(serializer, 'errors'):
                print(f"Erros de validação: {serializer.errors}")
            raise

    def perform_create(self, serializer):
        """Create a new medication"""
        print('entra aq')
        logger.info(f"📥 Dados recebidos para criação: {self.request.data}")
        serializer.save()

    def perform_update(self, serializer):
        """Update an existing medication"""
        serializer.save()

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a medication (soft delete)"""
        drug = self.get_object()
        drug.ativo = False
        drug.save()
        return Response({'status': 'medication deactivated'})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a medication"""
        drug = self.get_object()
        drug.ativo = True
        drug.save()
        return Response({'status': 'medication activated'})

    def destroy(self, request, *args, **kwargs):
        """Soft delete a medication"""
        drug = self.get_object()
        drug.delete()  # This will use the SoftDeleteModel's delete method
        return Response(status=status.HTTP_204_NO_CONTENT) 