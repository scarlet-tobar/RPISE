from flask import Flask
from db.db_connection import postgres_connection

app = Flask(__name__)
connection = postgres_connection()

@app.route('/set/horario', methods=['POST'])
def set_horario(id_estanque, hora_inicio, hora_termino):
    print('horario inicio:', hora_inicio)
    print('horario_termino:', hora_termino)
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("UPDATE estanque set hora_encendido=%s ,hora_apagado= %s where id_estanque =%s", (hora_inicio, hora_termino, id_estanque))
        print('se cambio el horario de: ', id_estanque)
    else:
        print('No se pudo establecer la conexión a la base de datos')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

connection.close()
print('Conexión cerrada')
