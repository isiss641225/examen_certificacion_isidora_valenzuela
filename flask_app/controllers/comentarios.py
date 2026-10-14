from flask import redirect, request, session
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario

@app.route('/cine/<int:id>/comentar', methods=['POST'])
def agregar_comentario(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.get_by_id(id)
    if pelicula and pelicula.usuario_id == session['usuario_id']:
        return redirect(f'/cine/{id}')

    if request.form['contenido']:
        data = {
            'contenido': request.form['contenido'],
            'usuario_id': session['usuario_id'],
            'pelicula_id': id
        }
        Comentario.save(data)

    return redirect(f'/cine/{id}')

@app.route('/comentario/borrar/<int:id>')
def borrar_comentario(id):
    if 'usuario_id' not in session:
        return redirect('/')

    comentario = Comentario.get_by_id(id)
    if comentario and comentario['usuario_id'] == session['usuario_id']:
        peli_id = comentario['pelicula_id']
        Comentario.delete(id)
        return redirect(f'/cine/{peli_id}')

    return redirect('/cine')