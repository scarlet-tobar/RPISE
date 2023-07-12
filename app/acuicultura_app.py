from db.db_connection import postgres_connection

connection = postgres_connection()

def set_horario(id_estanque, hora_inicio, hora_termino):
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("UPDATE estanque set hora_encendido=%s ,hora_apagado= %s where id_estanque =%s", (hora_inicio, hora_termino, id_estanque))
        print('se cambio el horario de: ', id_estanque)
        
    else:
        print('No se pudo establecer la conexión a la base de datos')

connection.close()
print('Conexión cerrada')