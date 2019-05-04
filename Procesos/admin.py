import csv
from django.http import HttpResponse
from django.contrib import admin

# Register your models here.

from Procesos.models import PeriodoProceso
from Procesos.procesos import run_acumuladosMensuales

class PeriodoAdminABC(admin.ModelAdmin):
    list_display = ('condominio', 'fecha_inicial', 'fecha_final')
    actions = ['acumulados']

    def acumulados(self, request, queryset):
        for obj in queryset:
            #field_value = getattr(obj, 'condominio')
            #print(" genera acumulados %s " % obj.condominio)
            run_acumuladosMensuales(obj.condominio)
        self.message_user(request, " Fin del proceso de generacion de acumulados ")

admin.site.register(PeriodoProceso, PeriodoAdminABC)

