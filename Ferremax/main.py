from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
import os
import uuid 
app = Flask(__name__)

CORS(app)
app.config['UPLOAD_FOLDER'] = 'upload'  # Carpeta donde se almacenan las imágenes subidas
# Lista de extensiones permitidas
extensiones_permitidas = {'jpg', 'jpeg', 'png', 'gif'}

# Subir foto
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
# def ver_foto(nombre_foto):
#     ruta_foto = os.path.join('upload', nombre_foto)
#     if not os.path.exists(ruta_foto):
#         return jsonify({'error': 'Foto no encontrada'}), 404    
#     with open(ruta_foto, 'rb') as f:
#         foto_contenido = f.read()    
#     return foto_contenido, 200, {'Content-Type': 'image/jpeg'}

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
