from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        session['reg_data'] = request.form
        return redirect('/')

    # Encriptar la contraseña antes de guardar en MySQL
    password_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password": password_hash
    }

    usuario_id = Usuario.save(data)
    session['usuario_id'] = usuario_id
    session.pop('reg_data', None)

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    usuario = Usuario.get_by_email(request.form['email'])

    # Verificar existencia y comparar contraseña desencriptando con Bcrypt
    if not usuario or not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("E-mail o contraseña incorrectos.", "login_error")
        session['login_email'] = request.form['email']
        return redirect('/')

    session['usuario_id'] = usuario.id
    session.pop('login_email', None)

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')