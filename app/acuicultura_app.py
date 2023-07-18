from flask import Flask, request
from db.db_connection import postgres_connection
import utils.colorAgua as CA
import utils.gpio as gpio
from utils.env import GPIO_OUT_PINS

app = Flask(__name__)
connection = postgres_connection()

current_id_estanque = None
current_hora_inicio = None
current_hora_termino = None
current_luz = None

@app.route('/set/horario', methods=['POST'])
def set_horario():
    data = request.json
    id_estanque = data.get('id_estanque')
    hora_inicio = data.get('hora_inicio')
    hora_termino = data.get('hora_termino')

    cursor = connection.cursor()
    cursor.execute("UPDATE estanque SET hora_encendido = %s, hora_apagado = %s WHERE id_estanque = %s", (hora_inicio, hora_termino, id_estanque))
    connection.commit()


    current_id_estanque = id_estanque
    current_hora_inicio = hora_inicio
    current_hora_termino = hora_termino

    print('Se cambió el horario de:', id_estanque)
    return "Horario actualizado"

@app.route('/set/luz', methods=['POST'])
def set_luz():
    data = request.json
    luz = data.get("luz")  # debe ser bool

    gpio.named_output("AC_LIGHT", bool(luz))
    # CA.enviarEstadoAgua()

    print('Se cambió la luz a:', luz)
    return "Luz actualizada"

@app.route('/set/medicion', methods=['POST'])
def set_medicion():
    id_estanque = request.json.get('id_estanque') #Obtiene el id_estanque que hace la medicion
    data = CA.enviarEstadoAgua() #Obtiene array con Datetime, turbiedad, anomalía, luz en una lista
    cursor = connection.cursor()
    cursor.execute("INSERT INTO medicion (id_estanque, luz, nivel_turbiedad, nivel_maduracion, anomalia, fecha_medicion) VALUES (%s, %s, %s, %s, %s, %s)", (id_estanque, data[3], data[1], data[1], data[2], data[0]))
    connection.commit()

    print("Se realizo medicion con los datos: ", data)
    return "Medición realizada"

if __name__ == '__main__':
    if connection is not None:
        gpio.init()
        app.run(host='0.0.0.0', port=2000)
    else:
        print('No se pudo establecer la conexión a la base de datos')

gpio.cleanup()
connection.close()
print('Conexión cerrada')
