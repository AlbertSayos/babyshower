from pymongo import MongoClient
from dotenv import load_dotenv
import os
import csv

# Cargar las variables de entorno del archivo .env
load_dotenv()

PORT = 8080

# Configuración de la base de datos MongoDB
mongo_uri = os.getenv("MONGO_CADENACONECCION")
mongo_db_name = os.getenv("MONGO_DB")
mongo_collection_name_no_repetibles = os.getenv("MONGO_REGALOSNOREPETIBLES")
mongo_collection_name_repetibles = os.getenv("MONGO_REGALOSREPETIBLES")

client = MongoClient(mongo_uri)
db = client[mongo_db_name]
collection_no_repetibles = db[mongo_collection_name_no_repetibles]
collection_repetibles = db[mongo_collection_name_repetibles]

def cargar_datos(nombre_archivo, coleccion):
    with open(nombre_archivo, newline='', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        print(f"Nombres de las columnas para {nombre_archivo}: {reader.fieldnames}")
        for row in reader:
            document = {
                'compras': row['COMPRAS '].strip(),
                'descripcion': row['DESCRIPCION'].strip(),
                'meAnoto': bool(row['ME ANOTO'].strip()),  # Convertir a booleano
                'link': row['LINK'].strip()
            }
            coleccion.insert_one(document)

def main():
    cargar_datos('regalosNoRepetibles.csv', collection_no_repetibles)
    cargar_datos('regalosRepetibles.csv', collection_repetibles)

if __name__ == '__main__':
    main()
