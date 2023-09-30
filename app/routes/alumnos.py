from flask import Blueprint, render_template

from ..models.AlumnosModels import AlumnoModel

alumnos_bp = Blueprint('alumnos', __name__)

@alumnos_bp.route('/alumnos')
def alumnos():
    alumnos = AlumnoModel.views_Alumnos()
    grupos = AlumnoModel.views_grupos()
    return render_template('alumnos.html', grupos=grupos, alumnos=alumnos )




@alumnos_bp.route("/alumno/view-clases/<id>")
def view_clase_alumno(id):
    datos = AlumnoModel.viws_clases_alumnos(id)
    return render_template("clases-alumno.html", datos=datos)

# <h5>{{ dato.4.strftime('%d-%m-%Y') }}</h5>

@alumnos_bp.route("/grupo/view-clases/<id>")
def view_clase_grupo(id):
    datos = AlumnoModel.viws_clases_grupo(id)
    return render_template("clases-grupo.html", datos=datos)
