setUp y tearDown:

setUp: Se ejecuta antes de cada prueba. Configura la aplicación Flask para pruebas y crea un cliente de prueba.
tearDown: Se ejecuta después de cada prueba. Limpia los archivos subidos para asegurar que cada prueba comienza con un estado limpio.
test_subir_foto:

Prueba subir una foto válida y verifica que la respuesta sea correcta y contenga el nombre del archivo subido.
test_subir_foto_sin_archivo:

Prueba subir sin enviar un archivo y verifica que se devuelva un error adecuado.
test_subir_foto_extension_no_permitida:

Prueba subir un archivo con una extensión no permitida y verifica que se devuelva un error adecuado.
test_ver_foto:

Prueba ver una foto existente. Primero sube una foto y luego intenta acceder a ella.
test_ver_foto_no_existente:

Prueba ver una foto que no existe y verifica que se devuelva un error adecuado.
test_eliminar_foto:

Prueba eliminar una foto existente. Primero sube una foto y luego intenta eliminarla.
test_eliminar_foto_no_existente:

Prueba eliminar una foto que no existe y verifica que se devuelva un error adecuado.