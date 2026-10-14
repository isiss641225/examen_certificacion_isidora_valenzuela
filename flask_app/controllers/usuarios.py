from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

# Inicialización de Bcrypt para el manejo seguro de contraseñas
bcrypt = Bcrypt(app)

# Ruta raíz: Muestra el formulario de ingreso/registro o redirige al catálogo si existe sesión
@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/cine')
    return render_template('index.html')

# Ruta POST: Procesa el registro de nuevos usuarios
@app.route('/registro', methods=['POST'])
def registro():
    # Validación de los datos del formulario de registro
    if not Usuario.validar_registro(request.form):
        session['reg_data'] = request.form
        return redirect('/')

    # Encriptación de la contraseña antes de almacenarla
    password_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password": password_hash
    }

    # Guardar usuario en BD y almacenar variables en la sesión activa
    usuario_id = Usuario.save(data)
    session['usuario_id'] = usuario_id
    session['usuario_nombre'] = request.form['nombre']  # Guardamos el nombre al registrarse
    session.pop('reg_data', None)

    return redirect('/cine')

# Ruta POST: Procesa la autenticación del usuario (Login)
@app.route('/login', methods=['POST'])
def login():
    usuario = Usuario.get_by_email(request.form['email'])

    # Verificación de credenciales y comparación de hash de contraseña
    if not usuario or not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("E-mail o contraseña incorrectos.", "login_error")
        session['login_email'] = request.form['email']
        return redirect('/')

    # Inicio de sesión exitoso: Guarda datos clave en sesión
    session['usuario_id'] = usuario.id
    session['usuario_nombre'] = usuario.nombre  # Guardamos el nombre al iniciar sesión
    session.pop('login_email', None)

    return redirect('/cine')

# Ruta GET: Destruye la sesión actual para salir del sistema
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')