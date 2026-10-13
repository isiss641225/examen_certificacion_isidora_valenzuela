from flask import Flask, session
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "clave_secreta_cinepedia"

bcrypt = Bcrypt(app)
DATABASE = 'cinepedia_db'