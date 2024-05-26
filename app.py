from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

PORT = 8080

app = Flask(__name__)

# Configuración de la base de datos MongoDB
mongo_uri = os.getenv("MONGO_CADENACONECCION")
mongo_db_name = os.getenv("MONGO_DB")
mongo_collection_name = os.getenv("MONGO_TABLA")

client = MongoClient(mongo_uri)
db = client[mongo_db_name]
collection = db[mongo_collection_name]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/invitacion/<nombre>')
def perfil(nombre):
    # Buscar el perfil por nombre
    result = collection.find_one({"nomFamilia": nombre})
    
    if result:
        return render_template('perfil.html', nombre=result['nomFamilia'], asistencia=result['asistencia'])
    else:
        return "Perfil no encontrado", 404

@app.route('/update_asistencia', methods=['POST'])
def update_asistencia():
    data = request.get_json()
    nombre = data['nombre']
    
    # Actualizar la asistencia
    result = collection.find_one_and_update(
        {"nomFamilia": nombre},
        {"$set": {"asistencia": not collection.find_one({"nomFamilia": nombre})["asistencia"]}},
        return_document=True
    )
    
    if result:
        return jsonify({'asistencia': result['asistencia']})
    else:
        return jsonify({'error': 'No se pudo actualizar la asistencia'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
