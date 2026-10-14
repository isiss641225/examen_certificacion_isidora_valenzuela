from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

# Clase Pelicula para gestionar todas las operaciones CRUD de películas en la base de datos
class Pelicula:
    # Constructor de la clase Pelicula
    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.director = data['director']
        self.fecha_estreno = data['fecha_estreno']
        self.sinopsis = data['sinopsis']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # Atributo opcional cargado mediante JOIN con la tabla usuarios
        if 'creador_nombre' in data:
            self.creador_nombre = data['creador_nombre']

    # Método de clase para registrar una nueva película
    @classmethod
    def save(cls, data):
        query = "INSERT INTO peliculas (titulo, director, fecha_estreno, sinopsis, usuario_id) VALUES (%(titulo)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # Método de clase para obtener todas las películas junto con el nombre del creador
    @classmethod
    def get_all(cls):
        query = "SELECT peliculas.*, usuarios.nombre AS creador_nombre FROM peliculas JOIN usuarios ON peliculas.usuario_id = usuarios.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        peliculas = []
        if results:
            for row in results:
                peliculas.append(cls(row))
        return peliculas

    # Método de clase para obtener una película específica por su ID
    @classmethod
    def get_by_id(cls, pelicula_id):
        query = "SELECT peliculas.*, usuarios.nombre AS creador_nombre FROM peliculas JOIN usuarios ON peliculas.usuario_id = usuarios.id WHERE peliculas.id = %(id)s;"
        data = {'id': pelicula_id}
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # Método de clase para actualizar la información de una película existente
    @classmethod
    def update(cls, data):
        query = "UPDATE peliculas SET titulo = %(titulo)s, director = %(director)s, fecha_estreno = %(fecha_estreno)s, sinopsis = %(sinopsis)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # Método de clase para eliminar una película de la base de datos por su ID
    @classmethod
    def delete(cls, pelicula_id):
        query = "DELETE FROM peliculas WHERE id = %(id)s;"
        data = {'id': pelicula_id}
        return connectToMySQL(DATABASE).query_db(query, data)

    # Método de clase para buscar una película por su título (útil en validaciones)
    @classmethod
    def get_by_titulo(cls, titulo):
        query = "SELECT * FROM peliculas WHERE titulo = %(titulo)s;"
        data = {'titulo': titulo}
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # Método estático para validar que los datos enviados en el formulario cumplan las reglas de negocio
    @staticmethod
    def validar_pelicula(formulario, peli_id=None):
        es_valido = True
        
        # Validación del título: longitud mínima y unicidad
        if len(formulario['titulo']) < 3:
            flash("El nombre debe tener al menos 3 caracteres", "err_titulo")
            es_valido = False
        else:
            peli_existente = Pelicula.get_by_titulo(formulario['titulo'])
            if peli_existente:
                if peli_id is None or peli_existente.id != int(peli_id):
                    flash("El nombre de la pelicula debe ser unico", "err_titulo")
                    es_valido = False

        # Validación del director
        if len(formulario['director']) < 3:
            flash("El director debe tener al menos 3 caracteres", "err_director")
            es_valido = False

        # Validación de la fecha de estreno
        if not formulario['fecha_estreno']:
            flash("La fecha de estreno no puede estar vacia", "err_fecha")
            es_valido = False

        # Validación de la sinopsis
        if not formulario['sinopsis'] or len(formulario['sinopsis']) < 3:
            flash("La sinopsis no puede estar vacia", "err_sinopsis")
            es_valido = False

        return es_valido