from flask import redirect, request, session, url_for
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario

@app.route('/cine/<int:id>/comentar', methods=['POST'])
def agregar_comentario(id):
    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    pelicula = Pelicula.get_by_id(id)
    # BONUS: Un usuario NO puede comentar en su propia película
    if pelicula and pelicula.usuario_id == session['usuario_id']:
        return redirect(url_for('ver_pelicula', id=id))

    contenido = request.form.get('contenido', '').strip()
    if contenido:
        data = {
            'contenido': contenido,
            'usuario_id': session['usuario_id'],
            'pelicula_id': id
        }
        Comentario.save(data)

    return redirect(url_for('ver_pelicula', id=id))

@app.route('/comentario/borrar/<int:id>')
def borrar_comentario(id):
    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    comentario = Comentario.get_by_id(id)
    if comentario and comentario['usuario_id'] == session['usuario_id']:
        peli_id = comentario['pelicula_id']
        Comentario.delete(id)
        return redirect(url_for('ver_pelicula', id=peli_id))

    return redirect(url_for('dashboard'))