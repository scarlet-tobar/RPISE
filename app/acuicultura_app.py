from flask import Flask, request
from db.db_connection import postgres_connection

app = Flask(__name__)
connection = postgres_connection()

@app.route('/set/horario', methods=['POST'])
def set_horario():
    id_estanque = request.form.get('id_estanque')
    hora_inicio = request.form.get('hora_inicio')
    hora_termino = request.form.get('hora_termino')

    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("UPDATE estanque SET hora_encendido = %s, hora_apagado = %s WHERE id_estanque = %s", (hora_inicio, hora_termino, id_estanque))
        connection.commit()
        print('se cambió el horario de:', id_estanque)
    else:
        print('No se pudo establecer la conexión a la base de datos')

    return "Horario actualizado"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)

connection.close()
print('Conexión cerrada')
