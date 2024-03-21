from app import app, usuarios
from flask import Flask, render_template, request, redirect, session,url_for
import pymongo
@app.route("/")
def Login():
    """Ruta inicial

    Returns:
        Login: Esta funcion accede al login.html
    """
    return render_template ("login.html")

@app.route("/", methods=["POST"])
def login ():
    """Ruta inicial

    Returns:
        Login: En esta funcion entramos a la base de datos validamos el correo y la contraseña 
               mediante una consulta, luego validamos la sesion para que no permita el ingreso sin
               haber accedido
    """
    mensaje=None
    estado=None
    try:
        correo  = request.form["correo"]
        contraseña = request.form["contraseña"]
        consulta = {"correo":correo, "contraseña":contraseña}
        user = usuarios.find_one(consulta)
        if (user):
            session["correo"]=correo
            return redirect (url_for("home"))
        else:
            mensaje = "Datos no validos"   
    except pymongo.errors as error:
        mensaje = error
    return render_template("login.html",estado=estado,mensaje=mensaje)