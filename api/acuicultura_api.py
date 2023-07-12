from app.acuicultura_app import *
from flask import Flask

app = Flask(__name__)

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
