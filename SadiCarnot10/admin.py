import csv
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.templatetags.static import static
from django.utils.html import format_html
# Register your models here.

from Procesos.procesosSADI10 import run_determinacionSaldos

from SadiCarnot10.models     import Condomino, Estacionamiento, CuentaBanco, \
                                    DetalleMovimiento, Documento, Movimiento, \
                                    Registro, AcumuladoMes, CuotasCondominio

class dontLog:
    def log_deletion(self, **kwargs):
        return

class DetalleMovtoInlineB(admin.TabularInline):
	model = DetalleMovimiento
	fields = ['descripcion', 'monto', 'cuenta_contable', 'proveedor']
	#list_display = ('cuenta_contable',)
	#list_filter = (('cuenta_contable', admin.RelatedOnlyFieldListFilter),)

	def get_extra(self, request, obj=None, **kwargs):
		extra = 4
		#if(obj):
		#	return extra - DetalleMovimiento.objects.filter(id = request.id).count()
		return extra

	#def cuenta_ingreso(self, request, obj=None, **kwargs):
	#    return	CuentaContable.objects.filter(clave_mayor = '41')

@admin.register(Movimiento)
class MovtoAdminB(admin.ModelAdmin):
    list_display = ('id','fecha','concepto','retiro','deposito','condomino','detalle','conciliacion')
    #list_filter = ('fecha','condomino',)
    date_hierarchy = 'fecha'
    readonly_fields = ('detalle',)
    ordering = ('-fecha',)
    save_on_top = True
    inlines = [DetalleMovtoInlineB]
    actions = ['export_as_csv']

    def concepto(self, request, obj=None, **kwargs):
        return '%s %s' % (request.tipo_movimiento,request.descripcion)

    def detalle(self, request, obj=None, **kwargs):
        cantidades =  DetalleMovimiento.objects.filter(movimiento_id = request.id).values_list('monto', flat = True)
        total = sum(cantidades)
        return total

    def conciliacion(self, request, obj=None, **kwargs):
        cantidades =  DetalleMovimiento.objects.filter(movimiento_id = request.id).values_list('monto', flat = True)
        total = sum(cantidades)
        if(total != (request.retiro + request.deposito)):
            return False
        else:
            return True

    conciliacion.boolean = True

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Exportar Seleccion a CSV"

@admin.register(CuentaBanco)
class CuentaBancoAdminB(admin.ModelAdmin):
    list_display = ('banco','clabe','apoderado')

@admin.register(Condomino)
class CondominoAdminB(admin.ModelAdmin):
    list_display = ('depto','propietario','adeudo_inicio','cuotas','depositos','detalle','adeudo_actual','estado_cuenta','descarga')
    search_fields = ('depto','propietario','poseedor')
    actions = ['determina_saldos']

    def adeudo_inicio(self, request, obj=None, **kwargs):
        return "{:,}".format(request.adeudo_inicial)

    def cuotas(self, request, obj=None, **kwargs):
        cargos = request.cargos - request.adeudo_inicial
        return "{:,}".format(cargos)

    def depositos(self, request, obj=None, **kwargs):
        pagos = request.pagos
        return "{:,}".format(pagos)

    def adeudo_actual(self, request, obj=None, **kwargs):
        return "{:,}".format(request.saldo)


    def determina_saldos(self, request, queryset):
        for obj in queryset:
            #print(" determina saldos %s " % obj.depto)
            run_determinacionSaldos(obj)
        self.message_user(request, " Fin del proceso de determinacion de saldos ")
    
    determina_saldos.short_description = "Determinacion de Saldos"

@admin.register(Estacionamiento)
class EstacionamientoAdminB(admin.ModelAdmin):
	list_display = ('ubicacion',)

@admin.register(Documento)
class DocumentoAdminB(admin.ModelAdmin):
    list_display = ('tipo_documento','folio','fecha_expedicion','monto_total')

@admin.register(Registro)
class AuxiliarAdminAB(dontLog, admin.ModelAdmin):
    list_display = ('condomino','fecha','E','detalle_movimiento','Cargos','Depositos','Saldo')
    #list_filter = ('fecha', 'condomino',)
    #date_hierarchy = 'fecha'
    change_list_template = "admin/titulo_registros.html"
    ordering = ('-fecha',)

    def Depositos(self, request, obj=None, **kwargs):
        return "{:,}".format(request.debe)

    def Cargos(self, request, obj=None, **kwargs):
        return "{:,}".format(request.haber)

    def Saldo(self, request, obj=None, **kwargs):
        return "{:,}".format(request.saldo)

    def E(self, request, obj=None, **kwargs):
        icon = '''
            <svg width="16" height="16" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <defs>
                    <g id="right">
                        <path d="M1413 896q0-27-18-45l-91-91-362-362q-18-18-45-18t-45 18l-91 91q-18 18-18 45t18 45l189 189h-502q-26 0-45 19t-19 45v128q0 26 19 45t45 19h502l-189 189q-19 19-19 45t19 45l91 91q18 18 45 18t45-18l362-362 91-91q18-18 18-45zm251 0q0 209-103 385.5t-279.5 279.5-385.5 103-385.5-103-279.5-279.5-103-385.5 103-385.5 279.5-279.5 385.5-103 385.5 103 279.5 279.5 103 385.5z"/>
                    </g>
                </defs>
                <use xlink:href="#right" x="0" y="0" fill="#447e9b" />
            </svg>
        ''' 
        #text = format_html('<img src="{}" alt="view">', icon)
        if(request.debe > 0):
            #return _boolean_icon(True)
            return mark_safe('%s' % icon)
        else:
            return ""

    E.allow_tags = True 

@admin.register(CuotasCondominio)
class CuotasAdminAB(admin.ModelAdmin):
    list_display = ('descripcion', 'mes_inicial', 'mes_final', 'monto','cuenta_contable')
    ordering = ('-mes_inicial',)    

@admin.register(AcumuladoMes)
class AcumuladoAdminB(admin.ModelAdmin):
    list_display = ('cuenta_banco', 'mes','fecha_inicial', 'fecha_final', 'depositos','retiros', 'saldo')
    ordering = ('fecha_inicial', 'cuenta_banco',)
    #date_hierarchy = 'fecha_inicial'
    actions = ['export_as_csv']
    change_list_template = "admin/titulo_acumulados.html"

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Exportar Seleccion a CSV"

#admin.site.register(Movimiento, MovtoAdminB)
#admin.site.register(CuentaBanco, CuentaBancoAdminB)
#admin.site.register(Condomino, CondominoAdminB)
#admin.site.register(Estacionamiento, EstacionamientoAdminB)
#admin.site.register(Documento, DocumentoAdminB)
#admin.site.register(Asiento, AuxiliarAdminAB)
#admin.site.register(AcumuladoMes, AcumuladoAdminB)
#admin.site.register(CuotasCondominio, CuotasAdminAB)

