import csv
from django.http import HttpResponse
from django.contrib import admin

# Register your models here.

from Procesos.models         import PeriodoProceso
from Procesos.procesosSADI10 import run_acumMes_SADI10
from Procesos.procesosSADI81 import run_acumMes_SADI81

class PeriodoAdminABC(admin.ModelAdmin):
    list_display = ('condominio', 'fecha_inicial', 'fecha_final')
    actions = ['acumulados']

    def acumulados(self, request, queryset):
        for obj in queryset:
            #field_value = getattr(obj, 'condominio')
            #print(" genera acumulados %s " % obj.condominio)
            if str(obj.condominio) == 'SADICARNOT10':	
            	run_acumMes_SADI10(obj.condominio)

            elif str(obj.condominio) == 'SADICARNOT81':	
            	run_acumMes_SADI81(obj.condominio)

        self.message_user(request, " Fin del proceso de generacion de acumulados ")

    acumulados.short_description = "Acumulados por mes"    

admin.site.register(PeriodoProceso, PeriodoAdminABC)

