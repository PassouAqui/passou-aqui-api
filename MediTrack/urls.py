from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore


urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/inventory/', include('inventory.urls')),
    path('api/v1/accounts/', include('accounts.urls')),

]
