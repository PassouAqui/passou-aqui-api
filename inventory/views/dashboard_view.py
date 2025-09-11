from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from inventory.serializers.dashboard_serializer import DashboardSerializer

class DashboardView(APIView):
    """
    View para fornecer todos os dados necessários para o dashboard.
    Esta view retorna um conjunto completo de dados que inclui:
    - Total de medicamentos, localizações e itens no inventário
    - Distribuição de medicamentos por tarja
    - Distribuição por localização
    - Medicamentos próximos do vencimento
    - Medicamentos com estoque baixo
    - Últimas movimentações
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Retorna todos os dados necessários para o dashboard em uma única chamada.
        Os dados são otimizados para minimizar o número de queries ao banco de dados.
        """
        try:
            dashboard_data = DashboardSerializer.get_dashboard_data()
            serializer = DashboardSerializer(data=dashboard_data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Erro ao obter dados do dashboard: {str(e)}'},
                status=500
            ) 