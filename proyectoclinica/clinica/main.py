from flask import Flask, render_template, request, redirect
from clases.conexion import Conexion

app = Flask(__name__)

@app.route("/")
def clinica_iniciar():
    return render_template("Index.html")

####PACIENTES######
@app.route("/pacientes/registrar/")
def pacientes_registrar():
    return render_template("registroPacientes.html")

@app.route("/pacientes/guardar/", methods=["POST"])
def pacientes_guardar():
    nombre = request.form["nombre"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    id_citas = 1
    conexion = Conexion()  
    conexion_local = conexion.obtener_conexion()  
    with conexion_local.cursor() as cursor:
        cursor.execute(
            "INSERT INTO paciente (nombre, direccion, telefono, email, id_citas) VALUES (%s, %s, %s, %s, %s)",
            (nombre, direccion, telefono, email, id_citas)
        )
        conexion_local.commit()
        conexion_local.close()
    return "paciente registrado"


@app.route("/pacientes/mostrar/")
def paciente_mostrar():
    conexion = Conexion()
    conexion_local = conexion.obtener_conexion()
    with conexion_local.cursor() as cursor:
        cursor.execute("SELECT * FROM paciente")
        pacientes = cursor.fetchall()  
    conexion_local.close()
    return render_template("mostrarPacientes.html", pacientes=pacientes)  

@app.route("/pacientes/actualizar/<int:id>")
def pacientes_actualizar(id):
    conexion = Conexion()
    conexion_local = conexion.obtener_conexion() 
    with conexion_local.cursor() as cursor:
        cursor.execute("SELECT * FROM paciente WHERE id=%s", (id,))
        pacientes = cursor.fetchall()
    conexion_local.close()
    return render_template("actualizarPacientes.html", pacientes=pacientes)

@app.route("/pacientes/modificar/", methods=["POST"])
def pacientes_modificar():
    conexion = Conexion()
    conexion_local = conexion.obtener_conexion()
    nombre = request.form["nombre"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    id = request.form["id"]
    with conexion_local.cursor() as cursor:
        cursor.execute(
            "UPDATE paciente SET nombre=%s, direccion=%s, telefono=%s, email=%s WHERE id=%s",
            (nombre, direccion, telefono, email, id)
        )
        conexion_local.commit()
        conexion_local.close()
    return redirect("/pacientes/mostrar/")

@app.route("/pacientes/eliminar/<id>")
def pacientes_eliminar(id):
    conexion = Conexion()
    conexion_local = conexion.obtener_conexion()
    with conexion_local.cursor() as cursor:
        cursor.execute("DELETE FROM cita WHERE paciente_id = %s", (id,))
        cursor.execute("DELETE FROM paciente WHERE id=%s", (id,))
    conexion_local.commit()
    conexion_local.close()
    return redirect("/pacientes/mostrar")





####DOCTORES######


@app.route("/doctores/registrar/")
def doctores_registrar():
    return render_template("registroDoctores.html")

@app.route("/doctores/guardar/", methods=["POST"])
def doctores_guardar():
    nombre = request.form["nombre"]
    especialidad = request.form["especialidad"]
    telefono = request.form["telefono"]
    id_citas = 1
    conexion = Conexion()  
    conexion_local = conexion.obtener_conexion() 
    with conexion_local.cursor() as cursor:
        cursor.execute(
            "INSERT INTO doctor (nombre, especialidad, telefono,  id_citas) VALUES (%s, %s, %s, %s)",
            (nombre, especialidad, telefono, id_citas)
        )
        conexion_local.commit()
        conexion_local.close()
    return "doctor registrado"


@app.route("/doctores/mostrar/")
def doctores_mostrar():
    conexion = Conexion()
    conexion_local = conexion.obtener_conexion()
    with conexion_local.cursor() as cursor:
        cursor.execute("SELECT * FROM doctor")
        doctores = cursor.fetchall()  
    conexion_local.close()
    return render_template("mostrarDoctores.html", doctores=doctores)  

@app.route("/doctores/actualizar/<int:id>")
def doctores_actualizar(id):
    conexion = Conexion()
    conexion_local = conexion.obtener_conexion() 
    with conexion_local.cursor() as cursor:
        cursor.execute("SELECT * FROM doctor WHERE id=%s", (id,))
        doctores = cursor.fetchall()
    conexion_local.close()
    return render_template("actualizarDoctores.html", doctores=doctores)

@app.route("/doctores/modificar/", methods=["POST"])
def doctores_modificar():
    conexion = Conexion()
    conexion_local = conexion.obtener_conexion()
    nombre = request.form["nombre"]
    especialidad = request.form["especialidad"]
    telefono = request.form["telefono"]
    id = request.form["id"]
    with conexion_local.cursor() as cursor:
        cursor.execute(
            "UPDATE doctor SET nombre=%s, especialidad=%s, telefono=%s WHERE id=%s",
            (nombre, especialidad, telefono, id)
        )
        conexion_local.commit()
        conexion_local.close()
    return redirect("/doctores/mostrar/")

@app.route("/doctores/eliminar/<id>")
def doctores_eliminar(id):
    conexion = Conexion()
    conexion_local = conexion.obtener_conexion()
    with conexion_local.cursor() as cursor:
        cursor.execute("DELETE FROM cita WHERE doctor_id = %s", (id,))
        cursor.execute("DELETE FROM doctor WHERE id=%s", (id,))
    conexion_local.commit()
    conexion_local.close()
    return redirect("/doctores/mostrar")





####CITAS######

# Ruta para mostrar todas las citas
@app.route("/citas/mostrar/")
def citas_mostrar():
    conexion = Conexion()
    conexion_local = conexion.obtener_conexion()
    with conexion_local.cursor() as cursor:
        cursor.execute("""
            SELECT c.id, c.fecha, c.hora, p.nombre AS paciente_nombre, d.nombre AS doctor_nombre
            FROM cita c
            JOIN paciente p ON c.paciente_id = p.id
            JOIN doctor d ON c.doctor_id = d.id
        """)
        citas = cursor.fetchall()
    conexion_local.close()
    return render_template("mostrarCitas.html", citas=citas)

# Ruta para actualizar una cita específica
@app.route("/citas/actualizar/<int:id>")
def citas_actualizar(id):
    conexion = Conexion()
    conexion_local = conexion.obtener_conexion()
    with conexion_local.cursor() as cursor:
        cursor.execute("SELECT * FROM cita WHERE id=%s", (id,))
        cita = cursor.fetchone()
    conexion_local.close()
    return render_template("actualizarCitas.html", cita=cita)

# Ruta para modificar una cita
@app.route("/citas/modificar/<int:id>", methods=["POST"])
def citas_modificar(id):
    fecha = request.form["fecha"]
    hora = request.form["hora"]
    paciente_id = request.form["paciente"]
    doctor_id = request.form["doctor"]
    
    conexion = Conexion()
    conexion_local = conexion.obtener_conexion()
    with conexion_local.cursor() as cursor:
        cursor.execute(
            "UPDATE cita SET fecha=%s, hora=%s, paciente_id=%s, doctor_id=%s WHERE id=%s",
            (fecha, hora, paciente_id, doctor_id, id)
        )
        conexion_local.commit()
    conexion_local.close()
    
    return redirect("/citas/mostrar/")

# Ruta para eliminar una cita
@app.route("/citas/eliminar/<int:id>")
def citas_eliminar(id):
    conexion = Conexion()
    conexion_local = conexion.obtener_conexion()
    with conexion_local.cursor() as cursor:
        cursor.execute("DELETE FROM cita WHERE id=%s", (id,))
    conexion_local.commit()
    conexion_local.close()
    return redirect("/citas/mostrar/")

# Ruta para el formulario de registro de citas
@app.route("/citas/registrar/")
def citas_registrar():
    return render_template("registroCitas.html")

# Ruta para guardar una nueva cita
@app.route("/citas/guardar/", methods=["POST"])
def citas_guardar():
    fecha = request.form["fecha"]
    hora = request.form["hora"]
    paciente_id = request.form["paciente"]
    doctor_id = request.form["doctor"]
    
    conexion = Conexion()
    conexion_local = conexion.obtener_conexion()
    with conexion_local.cursor() as cursor:
        cursor.execute(
            "INSERT INTO cita (fecha, hora, paciente_id, doctor_id) VALUES (%s, %s, %s, %s)",
            (fecha, hora, paciente_id, doctor_id)
        )
        conexion_local.commit()
    conexion_local.close()
    return redirect("/citas/mostrar/")




####ADMINISTRADOR#####

@app.route("/administradores/mostrar/")
def administradores_mostrar():
    try:
        conexion = Conexion()
        conexion_local = conexion.obtener_conexion()
        with conexion_local.cursor() as cursor:
            cursor.execute("""
                SELECT id, username, password, tipo
                FROM administrador
            """)
            administradores = cursor.fetchall()
    finally:
        conexion_local.close()
    
    return render_template("mostrarAdministradores.html", administradores=administradores)

