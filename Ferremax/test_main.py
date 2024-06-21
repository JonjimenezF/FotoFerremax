import unittest
from main import app
import os
import io

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = 'upload'
        self.client = app.test_client()

    def tearDown(self):
        # Limpiar los archivos subidos después de cada prueba
        folder = app.config['UPLOAD_FOLDER']
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def test_subir_foto(self):
        data = {
            'foto': (io.BytesIO(b"test_image_data"), 'test.jpg')
        }
        response = self.client.post('/upload', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Foto subida correctamente', response.json['mensaje'])
        self.assertIn('nombre_foto', response.json)

    def test_subir_foto_sin_archivo(self):
        response = self.client.post('/upload', content_type='multipart/form-data', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('No se encontró ninguna foto en la solicitud', response.json['error'])

    def test_subir_foto_extension_no_permitida(self):
        data = {
            'foto': (io.BytesIO(b"test_image_data"), 'test.txt')
        }
        response = self.client.post('/upload', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Extensión de archivo no permitida', response.json['error'])

    def test_ver_foto(self):
        # Primero subimos una foto para que podamos verla después
        data = {
            'foto': (io.BytesIO(b"test_image_data"), 'test.jpg')
        }
        upload_response = self.client.post('/upload', content_type='multipart/form-data', data=data)
        nombre_foto = upload_response.json['nombre_foto']
        
        response = self.client.get(f'/foto/{nombre_foto}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'image/jpeg')

    def test_ver_foto_no_existente(self):
        response = self.client.get('/foto/no_existe.jpg')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Foto no encontrada', response.json['error'])

    def test_eliminar_foto(self):
        # Primero subimos una foto para que podamos eliminarla después
        data = {
            'foto': (io.BytesIO(b"test_image_data"), 'test.jpg')
        }
        upload_response = self.client.post('/upload', content_type='multipart/form-data', data=data)
        nombre_foto = upload_response.json['nombre_foto']
        
        response = self.client.delete(f'/eliminar_foto/{nombre_foto}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Foto eliminada correctamente', response.json['mensaje'])

    def test_eliminar_foto_no_existente(self):
        response = self.client.delete('/eliminar_foto/no_existe.jpg')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Foto no encontrada', response.json['error'])

if __name__ == '__main__':
    unittest.main()
