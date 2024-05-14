from flask import Flask
import pymongo

app = Flask(__name__)
app.config["UPLOAD_FOLDER"]="./static/img"

app.secret_key = 'clavesecretita'

miConexion= pymongo.MongoClient("mongodb://localhost:27017")

baseDatos = miConexion["Datosss"]

productos = baseDatos["productos"]
categoria = baseDatos["categorias"]
usuarios = baseDatos["usuarios"]

from controller.usuarioController import *
from controller.productoController import *



if __name__ == "__main__":
    app.run(debug=True, port=4000)