from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
import os
import uuid 
import requests
import json

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
app.config['UPLOAD_FOLDER'] = 'upload'  # Carpeta donde se almacenan las imágenes subidas
# Lista de extensiones permitidas
extensiones_permitidas = {'jpg', 'jpeg', 'png', 'gif'}


URL_SUPEBASE = 'https://dfrsqtseebonqtptjjck.supabase.co/rest/v1/'
supebaseheads = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRmcnNxdHNlZWJvbnF0cHRqamNrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTU0MDkyMDIsImV4cCI6MjAzMDk4NTIwMn0.A-bL8uaHjYsLNGw448ffmIC0KV4CmHS2yERlwCI-rao'

# Ruta para obtener todos los productos
@app.route('/obtener_productos', methods=['GET'])
def obtener_productos():
    headers = {'apikey': supebaseheads}
    response = requests.get(URL_SUPEBASE + 'PRODUCTO?select=*', headers=headers)
    return response.json(), response.status_code

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    producto = request.json
    headers = {'apikey': supebaseheads}
    # Convertimos el objeto producto a JSON antes de pasarlo a requests.post
    response = requests.post(URL_SUPEBASE + 'PRODUCTO?', json=producto, headers=headers)
     # Verificamos si la respuesta del servidor es válida
    print(response)
    if response.status_code == 201:
        try:
            # Intentamos obtener el JSON de la respuesta
            data = producto_max_id()
        except json.decoder.JSONDecodeError:
            # Si hay un error al decodificar el JSON, devolvemos un mensaje de error genérico
            return jsonify({'error': 'Error al procesar la respuesta del servidor'}), 500

        # Verificamos si la solicitud fue exitosa
        if response.ok:
            return jsonify(data), response.status_code
        else:
            # Si la solicitud no fue exitosa, devolvemos los detalles del error
            return jsonify({'error': data}), response.status_code
    else:
        # Si la respuesta del servidor no es válida, devolvemos un mensaje de error
        return jsonify({'error': 'Error en la respuesta del servidor'}), response.status_code

def producto_max_id():
    query = {
        "select": "*",
        "order": "id_producto.desc",
        "limit": 1
    }
    headers = {'apikey': supebaseheads}
    
    response = requests.get(f'{URL_SUPEBASE}PRODUCTO', headers=headers, params=query)
    
    if response.status_code == 200:
        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            return jsonify({'error': 'Error al procesar la respuesta del servidor'}), 500
        
        return data[0]
    else:
        return jsonify({'error': 'Error en la respuesta del servidor'}), response.status_code
    
# Ruta para eliminar un producto por ID
@app.route('/eliminar_producto/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    headers = {'apikey': supebaseheads}
    response = requests.delete(URL_SUPEBASE + f'PRODUCTO?id_producto=eq.{id}', headers=headers)
    return response.json(), response.status_code

@app.route('/upload', methods=['POST'])
def subir_foto():
    if 'foto' not in request.files:
        return jsonify({'error': 'No se encontró ninguna foto en la solicitud'}), 400
    
    foto = request.files['foto']
    if foto.filename == '':
        return jsonify({'error': 'Nombre de archivo no válido'}), 400
    
    if '.' not in foto.filename or foto.filename.rsplit('.', 1)[1].lower() not in extensiones_permitidas:
        return jsonify({'error': 'Extensión de archivo no permitida'}), 400
    
    nombre_unido = str(uuid.uuid4()) + '.' + foto.filename.rsplit('.', 1)[1].lower()
    if not os.path.exists('upload'):
        os.makedirs('upload')
    
    foto.save(os.path.join('upload', nombre_unido))    
    return jsonify({'mensaje': 'Foto subida correctamente', 'nombre_foto': nombre_unido}), 200

# Ruta para ver una foto
@app.route('/foto/<nombre_foto>', methods=['GET'])
def ver_foto(nombre_foto):
    ruta_foto = os.path.join('upload', nombre_foto)
    if not os.path.exists(ruta_foto):
        return jsonify({'error': 'Foto no encontrada'}), 404
    
    return send_file(ruta_foto, mimetype='image/jpeg')

# Ruta para eliminar una foto
@app.route('/eliminar_foto/<nombre_foto>', methods=['DELETE'])
def eliminar_foto(nombre_foto):
    ruta_foto = os.path.join('upload', nombre_foto)
    if not os.path.exists(ruta_foto):
        return jsonify({'error': 'Foto no encontrada'}), 404

    os.remove(ruta_foto)  # Eliminar la foto del sistema de archivos
    return jsonify({'mensaje': 'Foto eliminada correctamente'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
