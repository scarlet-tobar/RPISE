from db.db_connection import postgres_connection

connection = postgres_connection()

if connection is not None:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM medicion")
    connection.close()
    print('Conexión cerrada')
else:
    print('No se pudo establecer la conexión a la base de datos')

