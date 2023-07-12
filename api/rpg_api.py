import json
from db.db_connection import postgres_connection
from flask import Flask

app = Flask(__name__)
connection = postgres_connection()

if connection is not None:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM medicion")

    @app.route('/set/intensidad', methods=['GET','POST'])
    def setIntensidad():
        return "configurtando intensidad"

    @app.route('/set/horario', methods=['GET','POST'])
    def setHorario():
        return "configurtando horario"

    @app.route('/set/anormalidades', methods=['GET','POST'])
    def setAnormalidad():
        return "configurtando anormailidades"

    @app.route('/set/liquido', methods=['GET','POST'])
    def setLiquido():
        return "configurtando liquido"

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=105)

    connection.close()
    print('Conexión cerrada')
else:
    print('No se pudo establecer la conexión a la base de datos')

