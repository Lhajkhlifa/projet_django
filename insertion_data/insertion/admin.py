from django.contrib import admin
from . import models
class VehiculeAdmin(admin.ModelAdmin):
    #list_display = ('vin',)
    pass

admin.site.register(models.Vehicule, VehiculeAdmin)