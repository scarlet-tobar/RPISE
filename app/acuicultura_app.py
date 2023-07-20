from datetime import datetime
from flask import Flask, request,jsonify
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
    luz = data.get('luz')

    # Comprobar si los valores son iguales a los almacenados en caché
    cache_key = f'horario_{id_estanque}'
    cached_horario = cache.get(cache_key)

    if cached_horario and cached_horario.get('hora_inicio') == hora_inicio and cached_horario.get('hora_termino') == hora_termino and cached_horario.get('luz') == luz:
        return "El horario y el estado de luz son los mismos, no se realizó ningún cambio"

    now = datetime.now().time()
    before = datetime.strptime(hora_inicio,"%H:%M").time()
    after = datetime.strptime(hora_termino,"%H:%M").time()
    estado_luz= luz=="True"

    if (before > after):
        before,after=after,before
        estado_luz=not estado_luz

    if (before < now and now < after and luz):
        gpio.named_output("AC_LIGHT", estado_luz)
    else:
        gpio.named_output("AC_LIGHT", not estado_luz)

    print(luz, hora_inicio,hora_termino)

    cursor = connection.cursor()
    cursor.execute("UPDATE estanque SET hora_encendido = %s, hora_apagado = %s, luz_encendida= %s WHERE id_estanque = %s", (hora_inicio, hora_termino, estado_luz, id_estanque))
    connection.commit()

    # Actualizar los valores en caché
    cache.set(cache_key, {'hora_inicio': hora_inicio, 'hora_termino': hora_termino, 'luz': luz})

    print('Se cambió el horario de:', id_estanque)
    return " Horario actualizado"


# @app.route('/set/medicion', methods=['POST'])
# def set_medicion():
#     id_estanque = request.json.get('id_estanque') #Obtiene el id_estanque que hace la medicion
#     data = CA.enviarEstadoAgua() #Obtiene array con Datetime, turbiedad, anomalía, luz en una lista
#     cursor = connection.cursor()
#     cursor.execute("INSERT INTO medicion (id_estanque, luz, nivel_turbiedad, nivel_maduracion, anomalia, fecha_medicion) VALUES (%s, %s, %s, %s, %s, %s)", (id_estanque, data[3], data[1], data[1], data[2], data[0]))
#     connection.commit()

#     print("Se realizo medicion con los datos: ", data)
#     return "Medición realizada"

if __name__ == '__main__':
    if connection is not None:
        gpio.init()
        app.run(host='0.0.0.0', port=2000)
    else:
        print('No se pudo establecer la conexión a la base de datos')

gpio.cleanup()
connection.close()
print('Conexión cerrada')
