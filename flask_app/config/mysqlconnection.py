import pymysql.cursors
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Clase para gestionar la conexión y la ejecución de consultas con MySQL
class MySQLConnection:
    def __init__(self, db):
        # Establece la conexión utilizando variables de entorno o valores por defecto
        connection = pymysql.connect(
            host = os.environ.get("MYSQL_HOST", os.environ.get("DB_HOST", "localhost")),
            user = os.environ.get("MYSQL_USER", os.environ.get("DB_USER", "root")),
            password = os.environ.get("MYSQL_PASSWORD", os.environ.get("DB_PASSWORD", "1234")),
            db = db,
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor,
            autocommit = True
        )
        self.connection = connection

    # Método genérico para ejecutar sentencias SQL (SELECT, INSERT, UPDATE, DELETE)
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid # Retorna el ID generado
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result # Retorna la lista de resultados
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong", e)
                return False
            finally:
                self.connection.close() # Garantiza el cierre de la conexión

# Función auxiliar para instanciar la conexión a la base de datos
def connectToMySQL(db):
    return MySQLConnection(db)