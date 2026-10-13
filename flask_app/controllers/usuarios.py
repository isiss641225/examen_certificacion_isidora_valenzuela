from flask import render_template, redirect, request, session
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/cine')
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        return render_template('index.html', reg_data=request.form)

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': pw_hash
    }
    usuario_id = Usuario.save(data)
    
    session['usuario_id'] = usuario_id
    session['usuario_nombre'] = request.form['nombre']
    return redirect('/cine')

@app.route('/login', methods=['POST'])
def login():
    usuario = Usuario.validar_login(request.form)
    if not usuario:
        return render_template('index.html', login_email=request.form['email'])

    session['usuario_id'] = usuario.id
    session['usuario_nombre'] = usuario.nombre
    return redirect('/cine')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')