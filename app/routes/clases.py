from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime

# Models
from ..models.ClasesModels import ClasesModel
from ..models.AlumnosModels import AlumnoModel

clases_bp = Blueprint('clases', __name__)

@clases_bp.route('/clases')
def clases():
    estudiantes = AlumnoModel().views_Alumnos()
    grupos = AlumnoModel().views_grupos()
    return render_template('clases.html', estudiantes=estudiantes, grupos=grupos)



def form_task():
    tiempo = request.form.get('tiempo')

    fecha = request.form['fecha']
    tema = request.form.get('tema')
    descripcion= request.form.get("descripcion")

    return tiempo, fecha, tema, descripcion


@clases_bp.route('/clase/estudiante', methods=['GET', 'POST'])
def add_task_estudiante():
    if request.method == 'POST':
        estudiante_id = request.form.get('alumnoSelect')
        
        profesor_id =  session['id'] 
        dato_form = form_task()

        datos = dato_form, estudiante_id, profesor_id
        print(datos)
        affected_rows = ClasesModel().add_clases_alumno(datos)
        if affected_rows == 1:
            flash("Tu datos ha sido guardado.")
            return redirect(url_for("clases.clases")) 
        else:
            print("Algo Salio Mal")
        return redirect(url_for("clases.clases")) 
    else:
        return redirect(url_for("clases.clases")) 
    
@clases_bp.route('/clase/grupo', methods=['GET', 'POST'])
def add_task_grupo():
    if request.method == 'POST':
        grupo_id = request.form.get('grupoSelect')
        
        profesor_id =  session['id'] 
        dato_form = form_task()

        datos = dato_form, grupo_id, profesor_id

        affected_rows = ClasesModel().add_clases_grupo(datos)
        if affected_rows == 1:
            flash("Tu datos ha sido guardado.")
            return redirect(url_for("clases.clases")) 
        else:
            print("Algo Salio Mal")
        return redirect(url_for("clases.clases")) 
    else:
        return redirect(url_for("clases.clases")) 
    
