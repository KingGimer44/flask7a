from flask import Flask

from flask import render_template
from flask import request
import pusher

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula = request.form["txtMatriculaFA"];
    nombreapellido = request.form["txtNombreApellidoFA"];
    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"
    
@app.route("/evento", methods=["GET"])
def evento():
    pusher_client = pusher.Pusher(
        app_id='1767967',
        key='34091ea15b1a362fb38d',
        secret='9a986831a832e499c9e4',
        cluster='us2',
        ssl=True
    )
    
    pusher_client.trigger('conexion', 'evento', request.args)
