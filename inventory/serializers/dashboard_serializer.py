from rest_framework import serializers
from inventory.models.drug import Drug
from inventory.models.inventory import Inventory
from inventory.models.location import Location

class DashboardSerializer(serializers.Serializer):
    total_drugs = serializers.IntegerField()
    total_locations = serializers.IntegerField()
    total_inventory_items = serializers.IntegerField()
    
    # Distribuição por localização
    location_distribution = serializers.DictField(
        child=serializers.IntegerField()
    )
    
    # Medicamentos próximos do vencimento (30 dias)
    expiring_soon = serializers.ListField(
        child=serializers.DictField()
    )
    
    # Medicamentos com estoque baixo (menos de 10 unidades)
    low_stock = serializers.ListField(
        child=serializers.DictField()
    )
    
    # Últimas movimentações
    recent_movements = serializers.ListField(
        child=serializers.DictField()
    )
    
    @staticmethod
    def get_dashboard_data():
        """Método para obter todos os dados necessários para o dashboard"""
        from django.db.models import Count, Q
        from django.utils import timezone
        from datetime import timedelta
        
        # Data base para medicamentos próximos do vencimento
        thirty_days_from_now = timezone.now() + timedelta(days=30)
        
        # Obtém todos os dados necessários em uma única query
        dashboard_data = {
            'total_drugs': Drug.objects.count(),
            'total_locations': Location.objects.count(),
            'total_inventory_items': Inventory.objects.count(),
            
            # Distribuição por localização
            'location_distribution': dict(
                Inventory.objects.values('location__name')
                .annotate(count=Count('id'))
                .values_list('location__name', 'count')
            ),
            
            # Medicamentos próximos do vencimento
            'expiring_soon': list(
                Inventory.objects.filter(
                    expiration_date__lte=thirty_days_from_now,
                    expiration_date__gt=timezone.now()
                ).select_related('drug', 'location')
                .values(
                    'id', 'drug__nome', 'drug__tarja',
                    'location__name', 'expiration_date',
                    'quantity'
                )
            ),
            
            # Medicamentos com estoque baixo
            'low_stock': list(
                Inventory.objects.filter(quantity__lt=10)
                .select_related('drug', 'location')
                .values(
                    'id', 'drug__nome', 'drug__tarja',
                    'location__name', 'quantity'
                )
            ),
            
            # Últimas movimentações (últimas 10)
            'recent_movements': list(
                Inventory.objects.select_related('drug', 'location')
                .order_by('-updated_at')[:10]
                .values(
                    'id', 'drug__nome', 'location__name',
                    'quantity', 'updated_at', 'movement_type'
                )
            )
        }
        
        return dashboard_data 