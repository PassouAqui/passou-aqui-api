from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.views import LocationViewSet
from inventory.views.cart_views import CartViewSet
from inventory.views.drug_viewset import DrugViewSet
from inventory.views.dashboard_view import DashboardView
from inventory.views.records_view import RecordsViewSet

router = DefaultRouter()
router.register(r'drugs', DrugViewSet, basename='drug')
router.register(r'drugs', DrugViewSet, basename='drug')
router.register(r'locations', LocationViewSet)
router.register(r'carts', CartViewSet)
router.register(r'records', RecordsViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]