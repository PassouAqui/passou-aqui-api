from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from inventory.models import Drug
from inventory.serializers.drug_serializer import DrugSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone

class DrugViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing medications (Drugs)
    """
    serializer_class = DrugSerializer
    permission_classes = [IsAuthenticated]
    queryset = Drug.objects.all()

    def get_queryset(self):
        """
        Optionally filter by active status
        """
        queryset = Drug.objects.all()
        active = self.request.query_params.get('active', None)
        if active is not None:
            queryset = queryset.filter(ativo=active.lower() == 'true')
        return queryset

    def perform_create(self, serializer):
        """Create a new medication"""
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