from app import app, productos, categoria, baseDatos, usuarios
from flask import Flask, render_template, request, jsonify, redirect, url_for,session
import pymongo
import os
from bson.objectid import ObjectId
import base64
from io import BytesIO
from bson.json_util import dumps
from pymongo import MongoClient
from controller.usuarioController import *

@app.route('/home')

def home():
    """Funcion de la ruta home

    Returns:
        _type_: Esta funcion se encarga de buscar los productos en la base de datos
                almacenarlos en un array y mediante un bucle for buscar el id de 
                categorias que viene de otra coleccion para asi agregarla en la coleccion
                productos y retornar el producto agregado en el html encargado de esto.
    """
    if("correo"in session):
        
        listaProductos = productos.find()
        todos_productos = []
        for producto in listaProductos:
            cat = categoria.find_one({'_id': ObjectId(producto['categoria'])})
            if cat:
                producto['categoria'] = cat['nombre']
                todos_productos.append(producto)
        return render_template("listarProductos.html", productos=todos_productos)
    else:
        mensaje ="Debe ingresar con sus datos"
        return render_template("login.html",mensaje=mensaje)
        
@app.route ("/agregarProductos")
def vistaAgregarProducto():
    """Vista Agregar Productos

    Returns:
        agregarProductos: En esta funcion buscamos a las categorias y retornamos el html del formulario de agregar
                          Productos  
    """
    if("correo"in session):
        listaCategorias = categoria.find()
        return render_template("formulario.html",categorias=listaCategorias)
    else:
        mensaje ="Debe ingresar con sus datos"
        return render_template("login.html",mensaje=mensaje)

@app.route("/agregarProductos", methods=["POST"])
def agregarProducto():
    """funcion agregarProductos

    Returns:
        agregarProductos: Aqui llamamos a los campos de producto y a la estructura del JSON
                          declaramos una variable resultado que llama a la coleccion para insertar
                          un documento con la funcion insert_one, una ves ingresado validamos que si 
                          es coreecto le damos un id a producto cargamos la foto agragada en la carpeta 
                          Upload_Folder y el mensaje de agregado de ser incorrecto el mensaje de no agregado  
    """
    mensaje = None
    estado = False
    if("correo"in session):
        try:
            codigo =int(request.form["codigo"]) 
            nombre = request.form["nombre"]
            precio = int(request.form["precio"])
            idCategoria = request.form["categoria"]
            foto =request.files["imagen"]


            producto ={
                "codigo":codigo,
                "nombre":nombre,
                "precio":precio,
                "categoria":ObjectId(idCategoria)
            }

            resultado = productos.insert_one(producto)
            if (resultado.acknowledged):
                idProducto = resultado.inserted_id
                nombreFoto = f"{idProducto}.jpg"
                foto.save(os.path.join(app.config["UPLOAD_FOLDER"],nombreFoto))
                mensaje = "Producto Agregado Correctamente"
                estado = True
                return redirect (url_for("home"))
            else:
                mensaje="Problemas al agregar"

            return render_template ("/formulario.html",estado= estado, mensaje=mensaje,)


        except pymongo.errors as error:
            mensaje = error
            return error
    else:
        mensaje ="Debe ingresar con sus datos"
        return render_template("login.html",mensaje=mensaje)
    
    
    
@app.route("/editarProducto/<producto_id>", methods=["GET"])
def editar_producto(producto_id):
    """Ruta editar producto

    Args:
        producto_id (ObjectId): llama al parametro ObjectId del producto a editar

    Returns:
        editar producto: busca al producto mediante el id en una variable llamada producto
        luego validamos el producto si es encontrado buscamos la categoria y retornamos al html de no ser asi
        retornamos un mensaje de no encontrado
    """
    if "correo" in session:
        try:
            producto = productos.find_one({"_id": ObjectId(producto_id)})
            if producto:
                listaCategorias = categoria.find()
                return render_template("editarProducto.html", producto=producto, categorias=listaCategorias)
            else:
                return "Producto no encontrado."
        except pymongo.errors.PyMongoError as error:
            return f"Error al cargar el producto: {error}"
    else:
        mensaje = "Debe ingresar con sus datos"
        return render_template("login.html", mensaje=mensaje)
    
@app.route("/actualizarProducto/<producto_id>", methods=["POST"])
def actualizar_producto(producto_id):
    """Ruta actualizar Producto

    Args:
        producto_id (ObjectId): llamamos al id del documento producto a actualizar

    Returns:
        Actualizar Productos: llamamos a los campos de la coleccion de productos, creamos el Json del producto actualizado
        luego llamamos a la coleccion productos actualizando asi el producto, luego validamos si se actualiza la foto para asi retornar 
        a la ruta home de no ser correcta la validacion y busqueda de productos se manda un mensaje de error
    """
    if "correo" in session:
        try:
            codigo = int(request.form["codigo"]) 
            nombre = request.form["nombre"]
            precio = int(request.form["precio"])
            idCategoria = request.form["categoria"]
            foto = request.files["imagen"]

            producto_actualizado = {
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "categoria": ObjectId(idCategoria)
            }

            productos.update_one({"_id": ObjectId(producto_id)}, {"$set": producto_actualizado})

            if foto:
                nombreFoto = f"{producto_id}.jpg"
                foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))

            return redirect(url_for("home"))

        except pymongo.errors.PyMongoError as error:
            return f"Error al actualizar el producto: {error}"
    else:
        mensaje = "Debe ingresar con sus datos"
        return render_template("login.html", mensaje=mensaje)

    
@app.route("/eliminarProducto/<producto_id>", methods=["GET"])
def eliminar_producto(producto_id):
    """Ruta eliminar producto

    Args:
        producto_id (ObjectId): se llama el ObjectId del producto en la coleccion productos

    Returns:
        Eliminar: se llama al producto junto la funcion delete para asi borrar el producto, una vez borrado retornamos a la ruta
        home, de no ser encontrado va a salir el mensaje de error.
    """
    if("correo"in session):
        try:
            resultado = productos.delete_one({"_id": ObjectId(producto_id)})
            if resultado.deleted_count == 1:
                return redirect(url_for("home"))
            else:
                return "Producto no encontrado."
        except pymongo.errors.PyMongoError as error:
            return f"Error al eliminar el producto: {error}"
    else:
        mensaje ="Debe ingresar con sus datos"
        return render_template("login.html",mensaje=mensaje)

@app.route("/salir")
def salir():
    session.clear()
    mensaje="Se ha cerrado sesion"
    return render_template("login.html",mensaje=mensaje)