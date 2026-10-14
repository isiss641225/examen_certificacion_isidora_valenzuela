from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario

# Ruta GET: Panel principal que despliega todas las películas registradas
@app.route('/cine')
def dashboard():
    # Verificación de sesión activa
    if 'usuario_id' not in session:
        return redirect('/')
    peliculas = Pelicula.get_all()
    return render_template('dashboard.html', peliculas=peliculas)

# Ruta GET/POST: Renderiza el formulario o procesa la creación de una película
@app.route('/cine/nueva', methods=['GET', 'POST'])
def nueva_pelicula():
    if 'usuario_id' not in session:
        return redirect('/')

    if request.method == 'POST':
        # Validar los campos del formulario de la película
        if not Pelicula.validar_pelicula(request.form):
            return render_template('nueva.html', data=request.form)

        # Preparar diccionario de datos asociando el ID del usuario creador
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

# Ruta GET: Muestra la información detallada de una película y sus comentarios
@app.route('/cine/<int:id>')
def ver_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.get_by_id(id)
    if not pelicula:
        return redirect('/cine')

    # Carga de comentarios asociados a la película
    comentarios = Comentario.get_by_pelicula(id)
    return render_template('ver.html', pelicula=pelicula, comentarios=comentarios)

# Ruta GET/POST: Renderiza o procesa la actualización de una película existente
@app.route('/cine/editar/<int:id>', methods=['GET', 'POST'])
def editar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.get_by_id(id)
    # Control de acceso: Verificar que la película exista y pertenezca al usuario en sesión
    if not pelicula or pelicula.usuario_id != session['usuario_id']:
        return redirect('/cine')

    if request.method == 'POST':
        # Validación pasando el ID actual para evitar conflictos de título duplicado
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

# Ruta GET: Elimina un registro de película validando la autoría
@app.route('/cine/borrar/<int:id>')
def borrar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.get_by_id(id)
    # Confirmación de permisos antes de eliminar en la base de datos
    if pelicula and pelicula.usuario_id == session['usuario_id']:
        Pelicula.delete(id)

    return redirect('/cine')