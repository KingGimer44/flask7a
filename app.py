from flask import Flask
from markupsafe import escape

from flask import render_template
from flask import request

import pusher

import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()
    
    return render_template("app.html")
    
@app.route("/alumnos")
def alumnos():
    con.close()
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
    
    nombreapellido = request.form["txtNombreApellidoFA"];
    telefono = request.form["txtTelefonoFA"];
    
    return f"Nombre y Apellido: {Nombre_Apellido} Telefono: {Telefono} "

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_reservas ORDER BY Id_Reserva DESC")
    registros = cursor.fetchall()

    con.close()

    return registros

@app.route("/registrar", methods=["GET"])
def registrar():
    args = request.args
    pusher_client = pusher.Pusher(
        app_id='1767967',
        key='34091ea15b1a362fb38d',
        secret='9a986831a832e499c9e4',
        cluster='us2',
        ssl=True
    )

    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    
    sql = "INSERT INTO tst0_reservas (Id_Reserva, Nombre_Apellido, Telefono, Fecha_Hora) VALUES (%s, %s, %s, %s)"
    val = (args["Nombre_Apellido"], args["Telefono"], datetime.datetime.now(pytz.timezone("America/Matamoros")))
    cursor.execute(sql, val)

    con.commit()
    con.close()
 
    pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", args)
    return args
    
@app.route("/evento", methods=["GET"])
def evento():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()

    args = request.args

    sql = "INSERT INTO tst0_reservas (Nombre_Apellido, Telefono, Fecha_Hora) VALUES (%s, %s, %s)"
    val = (args["Nombre_Apellido"], args["Telefono"], datetime.datetime.now())
    cursor.execute(sql, val)
    
    con.commit()
    con.close()
    
    pusher_client = pusher.Pusher(
        app_id='1767967',
        key='34091ea15b1a362fb38d',
        secret='9a986831a832e499c9e4',
        cluster='us2',
        ssl=True
    )
    
    pusher_client.trigger('conexion', 'evento', request.args)
