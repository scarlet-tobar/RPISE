from app import acuicultura_app
from flask import Flask

app = Flask(__name__)

@app.route('/set/horario', methods=['POST'])
def setLuz(id_estanque, horario_inicio, horario_termino):
    print('horario inicio:', horario_inicio)
    print('horario_termino:', horario_termino)
    acuicultura_app.set_horario(id_estanque, horario_inicio, horario_termino)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
