from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import urllib.parse

# Cargar las variables de entorno del archivo .env
load_dotenv()

PORT = 8080

app = Flask(__name__)

# Configuración de la base de datos MongoDB
mongo_uri = os.getenv("MONGO_CADENACONECCION")
mongo_db_name = os.getenv("MONGO_DB")
mongo_collection_name_no_repetibles = os.getenv("MONGO_REGALOSNOREPETIBLES")
mongo_collection_name_repetibles = os.getenv("MONGO_REGALOSREPETIBLES")

client = MongoClient(mongo_uri)
db = client[mongo_db_name]
collection_no_repetibles = db[mongo_collection_name_no_repetibles]
collection_repetibles = db[mongo_collection_name_repetibles]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/regalos')
def mostrar_regalos():
    regalos_no_repetibles = list(collection_no_repetibles.find({}))
    regalos_repetibles = list(collection_repetibles.find({}))
    #regalos_para_html = [[regalo['compras'], regalo['descripcion'], regalo['link']] for regalo in regalos_repetibles]
    regalos_para_html = []
    i=0
    for regalo in regalos_no_repetibles:
        if not regalo["meAnoto"]:
            infoDeRegalo= [regalo['compras'], regalo['descripcion'], regalo['link'],i]
            i = i +1
            regalos_para_html.append(infoDeRegalo)
    for regalo in regalos_repetibles:
        if not regalo["meAnoto"]:
            infoDeRegalo= [regalo['compras'], regalo['descripcion'], regalo['link'],i]
            i = i +1
            regalos_para_html.append(infoDeRegalo)

    return render_template('regalos.html', lista=regalos_para_html)



@app.route('/regalar', methods=['POST'])
def regalar():
    data = request.get_json()  # Obtiene el cuerpo JSON de la solicitud
    if data is not None:
        regalos = data.get('regalos', [])  # Obtiene la lista de regalos del JSON
        for regalo in regalos:
            result = collection_no_repetibles.find_one({"compras": regalo})
            if result:
                # Actualiza el valor de 'meAnoto' a True
                print("lo cambie")
                collection_no_repetibles.update_one({"compras": regalo}, {"$set": {"meAnoto": True}}
)
        return jsonify({"message": "Regalos recibidos", "regalos": regalos}), 200
    else:
        return jsonify({"error": "Datos inválidos"}), 400
    

@app.route('/enviar', methods=['GET'])
def enviar():
    telefono = os.getenv("NUMTEL")
    mensaje = "Hola! 🤗 con gusto asistiré al Baby Shower 💝 de Gianna 👶🏻👑"
    mensaje_cifrado = urllib.parse.quote(mensaje)  # Codificar mensaje
    whatsapp_link = f"https://api.whatsapp.com/send?phone={telefono}&text={mensaje_cifrado}"
    return jsonify({'whatsapp_link': whatsapp_link})


@app.route('/aviso')
def aviso():
    return render_template('aviso.html')


@app.route('/pasarafalse')
def pasarafalse():
    # Obtiene todos los documentos de la colección
    regalos = collection_no_repetibles.find({})
    
    # Itera sobre los documentos y actualiza 'meAnoto' a False
    for regalo in regalos:
        # Actualiza el campo 'meAnoto' a False para este documento
        collection_no_repetibles.update_one({"_id": regalo["_id"]}, {"$set": {"meAnoto": False}})
    
    return jsonify({"message": "Regalos cambiados"}), 200

    
                                         

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
