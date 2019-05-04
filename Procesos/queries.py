
from django.db import connection
from explorer.models import Query

def q_saldo_inicial(id_consulta):
	consulta = Query.objects.get(id=id_consulta)
	return(consulta.sql)
 
''' 
		SELECT 	nombre,
       			round(periodo_procesos.saldo_inicial,2) as saldo_inicial
		FROM 	periodo_procesos,
     	 		condominio
		WHERE 	periodo_procesos.condominio_id = condominio.id
		AND   	nombre = '%s'
''' 

def q_acumulados_mes(id_consulta):
	consulta = Query.objects.get(id=id_consulta)
	return(consulta.sql)




'''
			SELECT 	nombre,
       				cuenta,
       				strftime('%m-%Y', fecha) as mes,
       				--date_format(fecha,'%m-%Y') AS mes,
       				MIN(sadi_movimiento.FECHA) AS fec_ini,
       				MAX(sadi_movimiento.FECHA) AS fec_fin,
       				round(SUM(sadi_movimiento.deposito),2) AS depositos,
       				round(SUM(sadi_movimiento.retiro),2) AS retiros,
       				round(sum(deposito) - sum(retiro),2) AS diferencia
			FROM 	sadi_movimiento,
     				sadi_cuenta_banco,
     				periodo_procesos,
     				condominio
			WHERE 	sadi_cuenta_banco.id = sadi_movimiento.cuenta_banco_id
  			AND 	FECHA >= periodo_procesos.fecha_inicial
  			AND 	FECHA <= periodo_procesos.fecha_final
  			AND 	sadi_cuenta_banco.condominio_id = periodo_procesos.condominio_id
  			AND 	sadi_cuenta_banco.condominio_id = condominio.id
			GROUP by 1,2,3
			ORDER by 2,4,3
'''
