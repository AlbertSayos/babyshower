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
mongo_collection_regalo = os.getenv("MONGO_REGALOS")

client = MongoClient(mongo_uri)
db = client[mongo_db_name]
collection = db[mongo_collection_name]
listaRegalos = db[mongo_collection_regalo]

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


@app.route('/regalos')
def regalos():
    lista = listaRegalos.find()
    print(lista)
    
    retorno = []
    for regalo in lista:
        if regalo["EsActivo"]:
            retorno.append(regalo["regalo"])
    print(retorno)
    return render_template('index.html')

@app.route('/update_asistencia', methods=['POST'])
def update_asistencia():
    data = request.get_json()
    nombre = data['nombre']
    
    # Actualizar la asistencia a True
    result = collection.find_one_and_update(
        {"nomFamilia": nombre},
        {"$set": {"asistencia": True}},
        return_document=True
    )
    
    if result:
        # Generar el enlace de WhatsApp con el mensaje predeterminado
        telefono = os.getenv("NUMTEL")
        mensaje = "Hola, estoy encantado de asistir a tu baby shower."
        whatsapp_link = f"https://api.whatsapp.com/send?phone={telefono}&text={mensaje}"
        
        return jsonify({'whatsapp_link': whatsapp_link})
    else:
        return jsonify({'error': 'No se pudo actualizar la asistencia'}), 404

@app.route('/enviar', methods=['GET'])
def enviar():
    telefono = os.getenv("NUMTEL")
    mensaje = "Hola, estoy encantado de asistir a tu baby shower."
    whatsapp_link = f"https://api.whatsapp.com/send?phone={telefono}&text={mensaje}"
    return jsonify({'whatsapp_link': whatsapp_link})

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
