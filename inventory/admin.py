from django.contrib import admin
from inventory.models import (Drug, Location)

class DrugAdmin(admin.ModelAdmin):
    list_display = ('nome', )

admin.site.register(Drug, DrugAdmin)
