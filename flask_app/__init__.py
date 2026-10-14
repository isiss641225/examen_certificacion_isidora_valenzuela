from flask import Flask, session
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "f4d7fbc3dcb5b0e0313c2c68a862950bdd733a39420577d0"

bcrypt = Bcrypt(app)
DATABASE = 'cinepedia_db'