from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario

@app.route('/cine')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    peliculas = Pelicula.get_all()
    return render_template('dashboard.html', peliculas=peliculas)

@app.route('/cine/nueva', methods=['GET', 'POST'])
def nueva_pelicula():
    if 'usuario_id' not in session:
        return redirect('/')

    if request.method == 'POST':
        if not Pelicula.validar_pelicula(request.form):
            return render_template('nueva.html', data=request.form)

        data = {
            'titulo': request.form['titulo'],
            'director': request.form['director'],
            'fecha_estreno': request.form['fecha_estreno'],
            'sinopsis': request.form['sinopsis'],
            'usuario_id': session['usuario_id']
        }
        Pelicula.save(data)
        return redirect('/cine')

    return render_template('nueva.html')

@app.route('/cine/<int:id>')
def ver_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.get_by_id(id)
    if not pelicula:
        return redirect('/cine')

    comentarios = Comentario.get_by_pelicula(id)
    return render_template('ver.html', pelicula=pelicula, comentarios=comentarios)

@app.route('/cine/editar/<int:id>', methods=['GET', 'POST'])
def editar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.get_by_id(id)
    if not pelicula or pelicula.usuario_id != session['usuario_id']:
        return redirect('/cine')

    if request.method == 'POST':
        if not Pelicula.validar_pelicula(request.form, peli_id=id):
            return render_template('editar.html', pelicula=request.form, peli_id=id)

        data = {
            'id': id,
            'titulo': request.form['titulo'],
            'director': request.form['director'],
            'fecha_estreno': request.form['fecha_estreno'],
            'sinopsis': request.form['sinopsis']
        }
        Pelicula.update(data)
        return redirect('/cine')

    return render_template('editar.html', pelicula=pelicula, peli_id=id)

@app.route('/cine/borrar/<int:id>')
def borrar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.get_by_id(id)
    if pelicula and pelicula.usuario_id == session['usuario_id']:
        Pelicula.delete(id)

    return redirect('/cine')

    