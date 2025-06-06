from django.urls import path, include # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore
from inventory.views import DrugViewSet, LocationViewSet
from inventory.views.cart_views import CartViewSet
from inventory.views.drug_viewset import DrugViewSet
from inventory.views.dashboard_view import DashboardView

router = DefaultRouter()
router.register(r'drugs', DrugViewSet, basename='drug')
router.register(r'locations', LocationViewSet)
router.register(r'carts', CartViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
