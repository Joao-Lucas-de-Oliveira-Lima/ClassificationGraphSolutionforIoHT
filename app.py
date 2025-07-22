from flask import Flask, jsonify, send_file, send_from_directory
from flasgger import Swagger
from Dao import DAO
from DBConnection import DBConnection
from DBInitialize import DBInitialize
from XMLCreate import xml_create
import graphFunctions as gF
import os
import platform

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = "saved_model"

# Inicializar Swagger
swagger = Swagger(app)

# Inicializar banco e DAO
db = DBInitialize()
dao = DAO(db.connection_db)
modelText = ""

@app.route('/')
def index():
    """
    Endpoint básico de status
    ---
    responses:
      200:
        description: Servidor está rodando
    """
    return 'execute'

@app.route('/UpdateGraphRequest/<id>')
def updateGraphRequest(id=None):
    """
    Atualiza ou consulta o estado do grafo
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID da ação (0 = consulta, 1 = limpa, 2 = atualiza)
    responses:
      200:
        description: Estado atualizado ou retornado
    """
    global modelText
    if id == '0':
        return modelText
    if id == '1':
        modelText = ''
        return modelText
    if id == '2':
        modelText = 'graph_update'
        return modelText
    else:
        return 'wrong'

@app.route('/OptimizeGraphRequest/<sensors>')
def optimizeGraphRequest(sensors):
    """
    Otimiza grafo com base em sensores
    ---
    parameters:
      - name: sensors
        in: path
        type: string
        required: true
        description: Sensores separados por "_"
    responses:
      200:
        description: Arquivo XML otimizado
    """
    global modelText
    sensors = sensors.split("_")
    graphOptimized = gF.optimizeGraph(dao, sensors)
    edgeSensorFeaturesO, edgeFeatureModelsO, edgeModelFinalStatesO = graphOptimized
    xml_create(edgeSensorFeaturesO, edgeFeatureModelsO, edgeModelFinalStatesO, "KnowledgeBaseOptimized")
    return downloadOptimizeGraph()

@app.route('/OptimizeGraphRequest/<sensors>/<percentage>')
def optimizeGraphRequestPercentage(sensors, percentage):
    """
    Otimiza grafo com sensores e porcentagem
    ---
    parameters:
      - name: sensors
        in: path
        type: string
        required: true
      - name: percentage
        in: path
        type: string
        required: true
    responses:
      200:
        description: Arquivo XML otimizado
    """
    global modelText
    sensors = sensors.split("_")
    graphOptimized = gF.optimizeGraph(dao, sensors, int(percentage) / 100)
    edgeSensorFeaturesO, edgeFeatureModelsO, edgeModelFinalStatesO = graphOptimized
    xml_create(edgeSensorFeaturesO, edgeFeatureModelsO, edgeModelFinalStatesO, "KnowledgeBaseOptimized")
    return downloadOptimizeGraph()

@app.route('/OptimizeGraphRequest/download.xml')
def downloadOptimizeGraph():
    """
    Faz download do arquivo otimizado
    ---
    responses:
      200:
        description: Download do arquivo XML
    """
    if platform.system() == "Windows":
        return send_file("download\\KnowledgeBaseOptimized.xml", as_attachment=True)
    return send_file("download//KnowledgeBaseOptimized.xml", as_attachment=True)

@app.route('/GraphRequest')
def downloadGraph():
    """
    Faz download do grafo original
    ---
    responses:
      200:
        description: Download do arquivo XML original
    """
    if platform.system() == "Windows":
        return send_file("download\\KnowledgeBase.xml", as_attachment=True)
    return send_file("download//KnowledgeBase.xml", as_attachment=True)

@app.route('/saved_model/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    """
    Faz download de arquivos do modelo salvo
    ---
    parameters:
      - name: filename
        in: path
        type: string
        required: true
    responses:
      200:
        description: Arquivo do modelo baixado
    """
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=filename)

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(port=3000)
