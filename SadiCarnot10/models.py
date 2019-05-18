from django.db import models
from Catalogos.models import Banco, Condominio, Proveedore, TipoDocumento, \
                             Situacion, TipoMovimiento, CuentaContable
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.utils.html import format_html

# Create your models here.

class Estacionamiento(models.Model):
    ubicacion = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.ubicacion)

    class Meta:
        managed = True
        db_table = 'sadi_estacionamiento'

class CuentaBanco(models.Model):
    cuenta = models.CharField(max_length=20)
    clabe = models.CharField(max_length=18)
    apoderado = models.CharField(max_length=60)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0, null=True, verbose_name = ('Saldo inicial'))
    fecha_saldo = models.DateField(blank=True, null=True)
    situacion = models.IntegerField(blank=True, null=True)
    banco = models.ForeignKey(Banco, related_name='sadi_banco_cuenta', on_delete=models.PROTECT)
    condominio = models.ForeignKey(Condominio, related_name='sadi_cuenta_condominio', on_delete=models.PROTECT)
    tipo_cuenta = models.CharField(max_length=20)

    def __str__(self):
        return '%s %s %s' % (self.condominio, self.clabe, self.apoderado[:10])

    class Meta:
        managed = True
        db_table = 'sadi_cuenta_banco'
        verbose_name_plural = "Cuentas bancarias"

class Condomino(models.Model):
    depto = models.CharField(max_length=15, blank=True, null=True)
    propietario = models.CharField(max_length=60, blank=True, null=True)
    poseedor = models.CharField(max_length=60, blank=True, null=True)
    ubicacion = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=25, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fecha_escrituracion = models.DateField(blank=True, null=True)
    referencia = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    adeudo_inicial = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    fecha_corte_saldo = models.DateField(blank=True, null=True)
    cargos = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True,default = 0)
    pagos  = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True,default = 0)
    saldo = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default = 0)
    condominio = models.ForeignKey(Condominio, related_name='sadi_condomino_condominio_id', on_delete=models.PROTECT)
    estacionamiento = models.ManyToManyField(Estacionamiento, related_name='sadi_condomino_estacionamiento_id')

    def __str__(self):
        return '%s %s' % (self.depto, self.poseedor)

    #http://127.0.0.1:8000/admin/c_olimpo/asiento/?condomino__id__exact=9

    def estado_cuenta(self):
        icon_url = static('admin/img/icon-viewlink.svg')
        text = format_html('<img src="{}" alt="view">', icon_url)
        return mark_safe('<a href="/admin/SadiCarnot10/registro/?condomino__id__exact=%d">%s</a>' % (self.id,text))

    #http://127.0.0.1:8000/admin/c_olimpo/movimiento/?condomino__id__exact=10

    def detalle(self):
        #return mark_safe('<a href="/admin/SadiCarnot10/movimiento/?condomino__id__exact=%d">Detalle</a>' % (self.id))
        icon_url = static('admin/img/icon-viewlink.svg')
        text = format_html('<img src="{}" alt="view">', icon_url)
        return mark_safe('<a href="/admin/SadiCarnot10/movimiento/?condomino__id__exact=%d">%s</a>' % (self.id,text))

    def descarga(self):
        text = '''
        <svg width="16" height="16" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <defs>
                <g id="down">
                    <path d="M1412 897q0-27-18-45l-91-91q-18-18-45-18t-45 18l-189 189v-502q0-26-19-45t-45-19h-128q-26 0-45 19t-19 45v502l-189-189q-19-19-45-19t-45 19l-91 91q-18 18-18 45t18 45l362 362 91 91q18 18 45 18t45-18l91-91 362-362q18-18 18-45zm252-1q0 209-103 385.5t-279.5 279.5-385.5 103-385.5-103-279.5-279.5-103-385.5 103-385.5 279.5-279.5 385.5-103 385.5 103 279.5 279.5 103 385.5z"/>
                </g>
            </defs>
            <use xlink:href="#down" x="0" y="0" fill="#447e9b" />
        </svg>
        '''
        return mark_safe('<a href="/explorer/6/download?format=csv&params=depto:\'%s\'">%s</a>' % (self.depto,text))


    estado_cuenta.allow_tags = True
    detalle.allow_tags = True
    descarga.allow_tags = True

    class Meta:
        managed = True
        db_table = 'sadi_condomino'
        ordering = ['depto']

class Documento(models.Model):
    folio = models.IntegerField(blank=False, null=False)
    fecha_expedicion = models.DateField()
    monto_total = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    notas = models.CharField(max_length=45, blank=True, null=True)
    situacion = models.ForeignKey(Situacion, blank=True, null=True, related_name='sadi_recibo_situacion_id', on_delete=models.PROTECT)
    tipo_documento = models.ForeignKey(TipoDocumento, blank=True, null=True, related_name='sadi_recibo_tipodoc_id', on_delete=models.PROTECT)

    def __str__(self):
        return '%d %s' % (self.folio, self.tipo_documento)

    class Meta:
        managed = True
        db_table = 'sadi_documento'

class Movimiento(models.Model):
    cuenta_banco = models.ForeignKey(CuentaBanco, related_name='sadi_movimiento_cuenta_id', default = 2, on_delete=models.PROTECT)
    fecha = models.DateField(blank=True, null=True)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, blank=True, null=True, related_name='sadi_movimiento_tipo_movimiento_id', on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    condomino = models.ForeignKey(Condomino, related_name='sadi_movimiento_condomino_id', on_delete=models.PROTECT)
    retiro = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    deposito = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=500)
    documento = models.ForeignKey(Documento, related_name='sadi_movimiento_documento_id', default=1, on_delete=models.PROTECT)

    def __str__(self):
        return u'%d %s %d %s' % (self.id, self.fecha.strftime('%d/%m/%Y'), self.deposito, self.descripcion[:15])

    class Meta:
        managed = True
        db_table = 'sadi_movimiento'
        ordering = ['fecha']    
        verbose_name_plural = "Movimientos bancarios"

class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey(Movimiento, verbose_name = ('Movto'), on_delete = models.CASCADE, related_name='sadi_mov_detalle')
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    monto = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    cuenta_contable =  models.ForeignKey(CuentaContable, verbose_name = ('Cuenta Contable Ingreso/Egreso'), on_delete = models.CASCADE, related_name='sadi_cta_detalle', limit_choices_to = Q(clave_mayor='41') | Q(clave_mayor='51') | Q(num_cuenta='2318'))
    proveedor = models.ForeignKey(Proveedore, verbose_name = ('Proveedor'), on_delete = models.CASCADE, related_name='sadi_prov_detalle')

    def __str__(self):
        return '%s %s %s' % (self.descripcion, self.monto, self.cuenta_contable)

    class Meta:
        managed = True
        db_table = 'sadi_detalle_movimiento'
        ordering = ['movimiento']

class Registro(models.Model):
    fecha = models.DateField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, blank=True, null=True, related_name='sadi_auxiliar_tipo_movimiento_id', on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    debe = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    haber = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    saldo = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    cuenta_contable =  models.ForeignKey(CuentaContable, verbose_name = ('Cuenta Contable'), on_delete = models.PROTECT, related_name='sadi_asiento_cuenta')
    condomino = models.ForeignKey(Condomino, related_name='sadi_auxiliar_condomino_id', default=67, on_delete=models.PROTECT)
    a_favor = models.ForeignKey(Proveedore, related_name='sadi_auxiliar_proveedor_id', default=1, on_delete=models.PROTECT)

    @property
    def detalle_movimiento(self):
         return "%s %s" % ( self.tipo_movimiento, self.descripcion )

    def __str__(self):
        return u'%d %s %d %d %s %s' % (self.id, self.fecha.strftime('%d/%m/%Y'), self.debe, self.haber, self.descripcion[:15], self.cuenta_contable)

    class Meta:
        managed = True
        db_table = 'sadi_registro'
        ordering = ['fecha']
        verbose_name_plural = "Registros"

class CuotasCondominio(models.Model):
    descripcion = models.CharField(max_length=30, blank=True, null=True)
    mes_inicial = models.DateField(blank=True, null=True)
    mes_final = models.DateField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    monto = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    cuenta_contable =  models.ForeignKey(CuentaContable, verbose_name = ('Cuenta Contable'), on_delete = models.CASCADE, related_name='sadi_cuota_cuenta')
    condomino = models.ManyToManyField(Condomino, related_name='sadi_cuotas_condomino_id')

    def __str__(self):
        return u'%s %s %s %d %s' % (self.descripcion, self.mes_inicial.strftime('%m-%Y'), self.mes_final.strftime('%m-%Y'), self.monto, self.cuenta_contable)

    class Meta:
        managed = True
        db_table = 'sadi_cuotas'
        ordering = ['mes_inicial']
        verbose_name_plural = "Cuotas del condominio"

class AcumuladoMes(models.Model):
    #quitar posterior
    condominio = models.CharField(max_length=45, blank=True, null=True)
    cuenta_banco = models.CharField(max_length=20, blank=True, null=True)
    mes = models.CharField(max_length=7, blank=True, null=True)
    fecha_inicial = models.DateField(blank=True, null=True)
    fecha_final = models.DateField(blank=True, null=True)
    depositos = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)
    retiros = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)

    def __str__(self):
        return u'%s %s %s %s %d %d %d' % (self.cuenta_banco,self.mes,self.fecha_inicial.strftime('%d/%m/%Y'), self.fecha_final.strftime('%d/%m/%Y'),self.depositos, self.retiros, self.saldo)
 
    class Meta:
        managed = True
        db_table = 'sadi_acumulado_mes'
        verbose_name_plural = "Acumulados mensuales"
