from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

# Clase Comentario para gestionar las opiniones de los usuarios sobre las películas
class Comentario:
    # Constructor de la clase Comentario
    def __init__(self, data):
        self.id = data['id']
        self.contenido = data['contenido']
        self.usuario_id = data['usuario_id']
        self.pelicula_id = data['pelicula_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # Atributo opcional cargado mediante JOIN con la tabla usuarios
        if 'autor_nombre' in data:
            self.autor_nombre = data['autor_nombre']

    # Método de clase para guardar un nuevo comentario en la base de datos
    @classmethod
    def save(cls, data):
        query = "INSERT INTO comentarios (contenido, usuario_id, pelicula_id) VALUES (%(contenido)s, %(usuario_id)s, %(pelicula_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # Método de clase para obtener todos los comentarios de una película en orden cronológico inverso
    @classmethod
    def get_by_pelicula(cls, pelicula_id):
        query = "SELECT comentarios.*, usuarios.nombre AS autor_nombre FROM comentarios JOIN usuarios ON comentarios.usuario_id = usuarios.id WHERE pelicula_id = %(pelicula_id)s ORDER BY comentarios.created_at DESC;"
        data = {'pelicula_id': pelicula_id}
        results = connectToMySQL(DATABASE).query_db(query, data)
        comentarios = []
        if results:
            for row in results:
                comentarios.append(cls(row))
        return comentarios

    # Método de clase para buscar un comentario específico por su ID
    @classmethod
    def get_by_id(cls, comentario_id):
        query = "SELECT * FROM comentarios WHERE id = %(id)s;"
        data = {'id': comentario_id}
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # Método de clase para eliminar un comentario por su ID
    @classmethod
    def delete(cls, comentario_id):
        query = "DELETE FROM comentarios WHERE id = %(id)s;"
        data = {'id': comentario_id}
        return connectToMySQL(DATABASE).query_db(query, data)