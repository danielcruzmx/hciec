from django.db import connection

def dictfetchall(cursor):
	desc = cursor.description
	if desc:
		return [
       		dict(zip([col[0] for col in desc],row))
       		for row in cursor.fetchall()
		]
	else:
		return None

def execsql(consulta):
	cursor = connection.cursor()
	print(consulta)
	cursor.execute(consulta)
	result_list = dictfetchall(cursor)
	cursor.close()
	return result_list
	