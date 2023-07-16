from flask import Flask, request
from db.db_connection import postgres_connection
import utils.colorAgua as CA
import utils.gpio as gpio
from utils.env import GPIO_OUT_PINS

app = Flask(__name__)
connection = postgres_connection()

@app.route('/set/horario', methods=['POST'])
def set_horario():
    data= request.json
    id_estanque = data['id_estanque']
    hora_inicio = data['hora_inicio']
    hora_termino = data['hora_termino']
    cursor = connection.cursor()
    cursor.execute("UPDATE estanque SET hora_encendido = %s, hora_apagado = %s WHERE id_estanque = %s", (hora_inicio, hora_termino, id_estanque))
    connection.commit()
    print('se cambió el horario de:', id_estanque)
    return "Horario actualizado"

@app.route('/set/luz', methods=['POST'])
def set_luz():
    data= request.json
    luz=data["luz"] #debe ser bool
    gpio.named_output("AC_LIGHT",bool(luz))
    #CA.enviarEstadoAgua()
    print('se cambió la luz a: '+ luz)
    return "luz actualizada"

if __name__ == '__main__':
    if connection is not None:
        app.run(host='0.0.0.0', port=2000)
    else:
        print('No se pudo establecer la conexión a la base de datos')


connection.close()
print('Conexión cerrada')
