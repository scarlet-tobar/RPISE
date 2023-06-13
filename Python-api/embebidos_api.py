import json
from flask import Flask

app = Flask(__name__)

@app.route('/set/medicion', methods=['GET','POST'])
def setMedicion():
    return "ingresando datos postgres"

@app.route('/set/intensidad', methods=['GET','POST'])
def setIntensidad():
    return "configurtando intensidad"

@app.route('/set/horario', methods=['GET','POST'])
def setHorario():
    return "configurtando intensidad"

@app.route('/set/anormalidades', methods=['GET','POST'])
def setAnormalidad():
    return "configurtando intensidad"

@app.route('/set/liquido', methods=['GET','POST'])
def setLiquido():
    return "configurtando intensidad"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
