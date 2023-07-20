from datetime import datetime
from flask import Flask, request, make_response
from flask_caching import Cache
from db.db_connection import postgres_connection
import utils.colorAgua as CA
import utils.gpio as gpio
import time

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

    if not (before < now and now < after ):
        estado_luz= not estado_luz

    gpio.named_output("AC_LIGHT", estado_luz)

    cursor = connection.cursor()
    cursor.execute("UPDATE estanque SET hora_encendido = %s, hora_apagado = %s, luz_encendida= %s WHERE id_estanque = %s", (before, after, estado_luz, id_estanque))
    connection.commit()

    # Actualizar los valores en caché
    cache.set(cache_key, {'hora_inicio': hora_inicio, 'hora_termino': hora_termino, 'luz': luz})

    print('Se cambió el horario de:', id_estanque)
    return " Horario actualizado"

@app.route('/update/luz', methods=['POST'])
def update_luz():
    data = request.json
    id_estanque = data.get('id_estanque')
    hora_inicio = data.get('hora_inicio')
    hora_termino = data.get('hora_termino')
    luz = data.get('luz')

    # Obtener el caché de luz
    cache_key = f'luz_{id_estanque}'
    cached_luz = cache.get(cache_key)

    if cached_luz is not None and cached_luz == luz:
        return "El estado de luz es el mismo, no se realizó ningún cambio"

    now = datetime.now().time()
    before = datetime.strptime(hora_inicio,"%H:%M").time()
    after = datetime.strptime(hora_termino,"%H:%M").time()
    estado_luz= luz=="True"

    if not (before < now and now < after ):
        estado_luz= not estado_luz
        gpio.named_output("AC_LIGHT", estado_luz)
        cursor = connection.cursor()
        cursor.execute("UPDATE estanque SET luz_encendida= %s WHERE id_estanque = %s", (estado_luz, id_estanque))
        connection.commit()
        cache[cache_key] = luz
        print("actualizado el estado de luz del estanque: ",id_estanque)

    return "revisado"

last_measure = 0
@app.route('/set/medicion', methods=['POST'])
def set_medicion():
    global last_measure
    if time.time() - last_measure < 5:
        print("Medicion no realizada")
        return make_response("Medición no realizada", 400)
    
    id_estanque = request.json.get('id_estanque') #Obtiene el id_estanque que hace la medicion
    water_status, is_black = CA.doWaterMeasure() #Obtiene array con Datetime, turbiedad, anomalía, luz en una lista
    cursor = connection.cursor()
    if is_black:
        cursor.execute("INSERT INTO anomalia (id_estanque, fecha,anomalia,descripcion) VALUES (%s,now(),%s,%s)", (id_estanque,True,"La fotografia capturada es oscura o negra"))
        #anomalia
    else:
        cursor.execute("INSERT INTO medicion (id_estanque, nivel_turbiedad,nivel_maduracion,fecha) VALUES (%s,0,%s,now())", (id_estanque,water_status))
    connection.commit()

    print("Se realizo medicion con los datos: ", water_status, is_black)
    last_measure = time.time()
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
