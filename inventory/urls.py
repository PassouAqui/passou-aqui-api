from django.urls import path, include # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore
from inventory.views import DrugViewSet, LocationViewSet

router = DefaultRouter()
router.register(r'drugs', DrugViewSet)
router.register(r'locations', LocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
