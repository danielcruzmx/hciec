#from Procesos.queries import q_saldo_inicial, q_acumulados_mes
#from SadiCarnot10.models import AcumuladoMes
from datetime import datetime, timedelta
from explorer.models import Query
from django.db import transaction
from django.db import connection
from SadiCarnot10.models import AcumuladoMes, Asiento, CuotasCondominio, Movimiento, Condomino
from Procesos.models import PeriodoProceso
from Catalogos.models import TipoMovimiento, CuentaContable, Proveedore

def dictfetchall(cursor):
	desc = cursor.description
	return [
       dict(zip([col[0] for col in desc],row))
       for row in cursor.fetchall()
	]

def execsql(consulta):
	cursor = connection.cursor()
	#print(consulta)
	cursor.execute(consulta)
	result_list = dictfetchall(cursor)
	cursor.close()
	return result_list

def run_acumuladosMensuales(condominio):
	print(" generando acumulados %s " % condominio)
	with transaction.atomic():
		
		if str(condominio) == 'SADICARNOT10':	
			#
			#Borra acumulados		
			n = execsql('delete from sadi_acumulado_mes')
			#
			#Trae saldo inicial de cada cuenta
			saldo_condominio = 0 
			rows = execsql(Query.objects.get(id=4).sql)
			#
			#Por cada cuenta
			for r in rows:
				saldo = float(r['saldo_inicial'])
				#
				#Agrega depositos y retiros por cuenta y mes
				rows2 = execsql(Query.objects.get(id=2).sql)
				for r2 in rows2:
					if r2['cuenta'] == r['cuenta']:
						saldo = round(saldo + float(r2['depositos']) - float(r2['retiros']),2) 
						
						print(r2['nombre'], r2['cuenta'], r2['mes'], r2['depositos'], r2['retiros'], saldo)

						reg = AcumuladoMes(condominio=str(condominio),cuenta_banco=r2['cuenta'], \
										   mes=r2['mes'],fecha_inicial=r2['fec_ini'], \
										   fecha_final=r2['fec_fin'],depositos=r2['depositos'], \
										   retiros=r2['retiros'],saldo=saldo)
						reg.save()

				saldo_condominio = saldo_condominio + saldo		
				print(saldo_condominio)
			#
			#Actualiza saldo en periodos	
			oPer = PeriodoProceso.objects.get(id=1)
			oPer.saldo_inicial=saldo_condominio
			oPer.save()

def run_determinacionSaldos(condomino):
	print(" determinando saldos %s " % condomino.depto)
	with transaction.atomic():
		tipo   = TipoMovimiento.objects.get(id=21)
		prop   = TipoMovimiento.objects.get(id=30)
		cuenta = CuentaContable.objects.get(id=82)
		prove  = Proveedore.objects.get(id=1)
		#
		#Borra asientos 
		n = execsql('delete from sadi_asiento where condomino_id = %s' % condomino.id)
		#
		#Agrega adeudo inicial
		if not condomino.depto == '0000':
			adeudo = condomino.adeudo_inicial
			reg = Asiento(fecha = condomino.fecha_corte_saldo, fecha_vencimiento=condomino.fecha_corte_saldo, \
							tipo_movimiento = tipo, descripcion='SALDO INICIAL A LA FECHA', \
							debe = 0, haber=adeudo, saldo=adeudo, cuenta_contable=cuenta, \
							condomino = condomino, a_favor = prove)
			reg.save()
		#
		#Agrega adeudos por cuotas
		rows = CuotasCondominio.objects.all().order_by('mes_inicial')
		for r in rows:
			delta = (r.mes_final - r.mes_inicial)
			#print(r.descripcion,r.mes_inicial,r.mes_final,r.monto,r.cuenta_contable,delta.days)
			condom = r.condomino.filter(depto__contains=condomino.depto)
			if condom:	
				base = r.mes_inicial
				for x in range (0, delta.days + 1):
					fecha = base + timedelta(days=x)
					if fecha.day == 1:
						reg = Asiento(fecha = fecha, fecha_vencimiento=fecha, \
								tipo_movimiento = tipo, descripcion=r.descripcion , \
								debe = 0, haber=r.monto, saldo=0, cuenta_contable=r.cuenta_contable, \
								condomino = condomino, a_favor = prove)
						reg.save()
		#
		#Agrega depositos por movimiento de banco
		if not condomino.depto == '0000':
			movtos = Movimiento.objects.filter(condomino__id=condomino.id)
			for m in movtos:
				reg = Asiento(fecha = m.fecha, fecha_vencimiento=m.fecha, \
						tipo_movimiento = m.tipo_movimiento, descripcion=m.descripcion , \
						debe = m.deposito, haber=0, saldo=0, cuenta_contable=r.cuenta_contable, \
						condomino = condomino, a_favor = prove)
				reg.save()
			#
			#Recalcula saldos
			saldo = 0
			cargos = 0
			depositos = 0
			rec = Asiento.objects.filter(condomino__id=condomino.id).order_by('fecha')
			for r in rec:
				cargos = cargos + r.haber
				depositos = depositos + r.debe
				saldo = saldo + r.haber - r.debe
				r.saldo = saldo
				r.save()
			
			reg = Condomino.objects.get(id=condomino.id)
			reg.cargos = cargos
			reg.pagos = depositos
			reg.saldo = saldo
			reg.save()
			
