from flask import redirect, request, session
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario

# Ruta POST: Procesa la creación de un nuevo comentario en una película
@app.route('/cine/<int:id>/comentar', methods=['POST'])
def agregar_comentario(id):
    # Verificación de sesión activa
    if 'usuario_id' not in session:
        return redirect('/')

    # Restricción de seguridad: El creador de la película no puede comentar en su propia publicación
    pelicula = Pelicula.get_by_id(id)
    if pelicula and pelicula.usuario_id == session['usuario_id']:
        return redirect(f'/cine/{id}')

    # Guardar comentario si el campo de texto no está vacío
    if request.form['contenido']:
        data = {
            'contenido': request.form['contenido'],
            'usuario_id': session['usuario_id'],
            'pelicula_id': id
        }
        Comentario.save(data)

    return redirect(f'/cine/{id}')

# Ruta GET: Elimina un comentario verificando la autoría del mismo
@app.route('/comentario/borrar/<int:id>')
def borrar_comentario(id):
    # Verificación de sesión activa
    if 'usuario_id' not in session:
        return redirect('/')

    comentario = Comentario.get_by_id(id)
    # Confirmar permisos: Solo el usuario dueño del comentario puede eliminarlo
    if comentario and comentario['usuario_id'] == session['usuario_id']:
        peli_id = comentario['pelicula_id']
        Comentario.delete(id)
        return redirect(f'/cine/{peli_id}')

    return redirect('/cine')