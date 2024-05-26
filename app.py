from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import psycopg2
from traerdato import stringConn

PORT = 8080

app = Flask(__name__)

# Configuración de la base de datos
"""
db_config = {
    'user': 'root',
    'password': '',  # Deja la contraseña vacía si no has configurado una
    'host': '127.0.0.1',
    'database': 'inivitaciones',
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection
"""


@app.route('/rata')
def rata():
    print(f"esta es la cadena de coneccion {stringConn}")
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/invitacion/<nombre>')
def perfil(nombre):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Buscar el perfil por nombre
    query = "SELECT * FROM invitaciones WHERE familia = %s"
    cursor.execute(query, (nombre,))
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if result:
        return render_template('perfil.html', nombre=result['familia'], asistencia=result['asistencia'])
    else:
        return "Perfil no encontrado", 404

@app.route('/update_asistencia', methods=['POST'])
def update_asistencia():
    data = request.get_json()
    nombre = data['nombre']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Actualizar la asistencia
    query = "UPDATE Invitaciones SET asistencia = NOT asistencia WHERE familia = %s"
    cursor.execute(query, (nombre,))
    connection.commit()
    
    # Obtener el nuevo estado de asistencia
    query = "SELECT asistencia FROM Invitaciones WHERE familia = %s"
    cursor.execute(query, (nombre,))
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return jsonify({'asistencia': result[0]})

if __name__ == "__main__":
    import os
    from gunicorn.app.wsgiapp import WSGIApplication

    os.environ["PORT"] = "8000"  # Puerto para tu aplicación Flask

    # Iniciar Gunicorn
    WSGIApplication("%(prog)s [OPTIONS]").run()
