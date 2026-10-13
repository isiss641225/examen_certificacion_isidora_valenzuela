from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = {'email': email}
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = {'id': user_id}
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validar_registro(formulario):
        es_valido = True
        
        if len(formulario['nombre']) < 2:
            flash("Nombre debe tener al menos 2 caracteres", "reg_nombre")
            es_valido = False
            
        if len(formulario['apellido']) < 2:
            flash("Apellido debe tener al menos 2 caracteres", "reg_apellido")
            es_valido = False
            
        if "@" not in formulario['email'] or len(formulario['email']) < 5:
            flash("Email invalido", "reg_email")
            es_valido = False
        else:
            usuario_existe = Usuario.get_by_email(formulario['email'])
            if usuario_existe:
                flash("El email ya esta registrado", "reg_email")
                es_valido = False

        if len(formulario['password']) < 1 or formulario['password'] != formulario['conf_password']:
            flash("Las contraseñas no coinciden", "reg_password")
            es_valido = False

        return es_valido

    @staticmethod
    def validar_login(formulario):
        usuario = Usuario.get_by_email(formulario['email'])
        if not usuario:
            flash("Email o contraseña incorrectos", "login_error")
            return False
        if not bcrypt.check_password_hash(usuario.password, formulario['password']):
            flash("Email o contraseña incorrectos", "login_error")
            return False
        return usuario