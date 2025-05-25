from django.urls import path, include # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore
from inventory.views import DrugViewSet, LocationViewSet
from inventory.views.cart_views import CartViewSet

router = DefaultRouter()
router.register(r'drugs', DrugViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'carts', CartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
