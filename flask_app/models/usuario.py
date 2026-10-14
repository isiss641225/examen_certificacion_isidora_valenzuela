from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    db = "cinepedia_db"

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
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password) 
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = {'email': email}
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = {'id': user_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validar_registro(data):
        is_valid = True

        if len(data['nombre'].strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "reg_nombre")
            is_valid = False

        if len(data['apellido'].strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "reg_apellido")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("E-mail inválido.", "reg_email")
            is_valid = False
        else:
            usuario_existente = Usuario.get_by_email(data['email'])
            if usuario_existente:
                flash("Este correo ya está registrado.", "reg_email")
                is_valid = False

        if len(data['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "reg_password")
            is_valid = False

        if data['password'] != data['conf_password']:
            flash("Las contraseñas no coinciden.", "reg_password")
            is_valid = False

        return is_valid