import time
from flask import Flask, request
from flask_caching import Cache
from db.db_connection import postgres_connection
import utils.colorAgua as CA
import utils.gpio as gpio

app = Flask(__name__)
cache = Cache(app)
connection = postgres_connection()

# Configuración de Flask-Caching
app.config['CACHE_TYPE'] = 'simple'  # Puedes usar otros tipos de caché según tus necesidades
cache.init_app(app)

@app.route('/set/horario', methods=['POST'])
def set_horario():
    data = request.json
    id_estanque = data.get('id_estanque')
    hora_inicio = data.get('hora_inicio')
    hora_termino = data.get('hora_termino')

    # Comprobar si los valores son iguales a los almacenados en caché
    cache_key = f'horario_{id_estanque}'
    cached_horario = cache.get(cache_key)

    if cached_horario and cached_horario.get('hora_inicio') == hora_inicio and cached_horario.get('hora_termino') == hora_termino:
        return "El horario es el mismo, no se realizó ningún cambio"

    now = time.time()
    print(hora_inicio,now , hora_termino)
    if (hora_inicio < now and now < hora_termino):
        gpio.named_output("AC_LIGHT",True)
    else:
         gpio.named_output("AC_LIGHT",False)

    cursor = connection.cursor()
    cursor.execute("UPDATE estanque SET hora_encendido = %s, hora_apagado = %s WHERE id_estanque = %s", (hora_inicio, hora_termino, id_estanque))
    connection.commit()

    # Actualizar los valores en caché
    cache.set(cache_key, {'hora_inicio': hora_inicio, 'hora_termino': hora_termino})

    print('Se cambió el horario de:', id_estanque)
    return "Horario actualizado"

@app.route('/set/luz', methods=['POST'])
def set_luz():
    data = request.json
    id_estanque = data.get('id_estanque')
    luz = data.get('luz')

    # Comprobar si el valor es igual al almacenado en caché
    cache_key = f'luz_{id_estanque}'
    cached_luz = cache.get(cache_key)

    if cached_luz == luz:
        return "La luz es la misma, no se realizó ningún cambio"
    gpio.named_output("AC_LIGHT", luz=="True")
    cursor = connection.cursor()
    cursor.execute("UPDATE estanque SET luz_encendida = %s WHERE id_estanque = %s", (luz, id_estanque))
    connection.commit()
    # Actualizar el valor en caché
    cache.set(cache_key, luz)

    print('Se cambió la luz de:', id_estanque)
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
