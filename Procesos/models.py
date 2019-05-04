from django.db import models
from django.db.models import Q

from Catalogos.models import Condominio

class PeriodoProceso(models.Model):
    condominio = models.ForeignKey(Condominio, on_delete=models.PROTECT)
    fecha_inicial = models.DateField(blank=True, null=True)
    fecha_final = models.DateField(blank=True, null=True)
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, verbose_name = ('Saldo final'))

    def __str__(self):
        return '%s' % (self.condominio)

    class Meta:
        managed = True
        db_table = 'periodo_procesos'
        verbose_name_plural = "Periodos"