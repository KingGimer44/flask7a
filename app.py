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
    com.close()
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    com.close()
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    com.close()
    
    matricula = request.form["txtMatriculaFA"];
    nombreapellido = request.form["txtNombreApellidoFA"];
    
    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * tst0_reservas")
    
    registros = cursor.fetchall()

    return registros;
    
@app.route("/evento", methods=["GET"])
def evento():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()

    args = request.args

    sql = "INSERT INTO sensor_log (Nombre_Apellido, Telefono, Fecha_Hora) VALUES (%s, %s, %s)"
    val = (args["Nombre_Apellido"], args["Telefono"], datetime.datetime.now())
    cursor.execute(sql, val)
    
    con.commit()
    com.close()
    
    pusher_client = pusher.Pusher(
        app_id='1767967',
        key='34091ea15b1a362fb38d',
        secret='9a986831a832e499c9e4',
        cluster='us2',
        ssl=True
    )
    
    pusher_client.trigger('conexion', 'evento', request.args)
