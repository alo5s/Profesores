from functools import wraps
from flask import Blueprint, render_template, session, redirect, request, url_for , flash

# Models
from ..models.AdminModels import AdminModel

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('admin.login_admin'))
        user_model = AdminModel()
        user = user_model.get_usuario_por_nombre(session['username'])
        if user and user.get('admin', False):
            return view_func(*args, **kwargs)
        return "Acceso no autorizado" 
    return decorated_view



@admin_bp.route("/logout")
def logout():
    session.pop('username', None)  
    return redirect("/admin/login")


@admin_bp.route('/login', methods=['POST', 'GET'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_model = AdminModel()
        user = user_model.get_usuario_por_nombre(username)

        if user and user['contraseña'] == password:  
            session['username'] = user['usuario']  
            return redirect(url_for("admin.add_profesor")) 
        return "Credenciales inválidas" 
    else:
        return render_template('/admin/auth/login.html')




@admin_bp.route('/home')
@admin_required
def home_admin():
    return render_template('/admin/home.html')

def add_form():
    dato_1 = request.form.get('dato-1')
    dato_2 = request.form.get('dato-2')
    return dato_1, dato_2



# PROFESORES

@admin_bp.route('/profesores')
@admin_required
def profesores_admin():
    datos = AdminModel().views_profesores()
    return render_template('/admin/profesor.html', datos=datos)

@admin_bp.route('/add_profesor', methods=['POST', 'GET'])
def add_profesor():
    if request.method == 'POST':
        datos_profesor = add_form()
        affected_rows = AdminModel().add_profesor(datos_profesor)
        if affected_rows == 1:
            flash("Tu datos ha sido guardado.")
            return redirect(url_for("admin.profesores_admin")) 
        else:
            print("Algo Salio Mal")
            return redirect(url_for("admin.profesores_admin")) 
    else :
        return redirect(url_for("admin.profesores_admin")) 

@admin_bp.route('/delete/profesor/<id>')
def delete_profesor(id):
    affected_rows = AdminModel().delete_profesor(id)
    if affected_rows == 1:
        flash("EL dato fue borrado")
        return redirect(url_for("admin.profesores_admin")) 
    else:
        print("Algo Salio Mal")
        return redirect(url_for("admin.profesores_admin")) 

@admin_bp.route('/updata/profesor/<id>', methods=['POST', 'GET'])
def updata_profesro(id):
    if request.method == 'POST':
        datos_profesor = add_form()
        affected_rows = AdminModel().update_profesor(datos_profesor, id)
        if affected_rows == 1:
            flash("Tu datos ha sido Actualizado.")
            return redirect(url_for("admin.profesores_admin")) 
        else:
            print("Algo Salio Mal")
            return redirect(url_for("admin.profesores_admin")) 
    else :
        return redirect(url_for("admin.profesores_admin")) 
  


@admin_bp.route('/profesor/clases/<id>')
def profesores_view_infor(id):
    datos = AdminModel.viws_clases_profesor(id)
    return render_template("/admin/view-tabla/index.html", datos=datos)
    


@admin_bp.route('/profesor/clases/estado/<tipo>/<id>')
def estado_clase(tipo, id):
    
    if tipo == "estudiante":
        affected_rows = AdminModel().validado_profesor_alumno(id)
        if affected_rows == 1:
            print("Tu datos ha sido guardado.")
            return redirect(request.referrer)
        else:
            print("Algo Salio Mal")
            return redirect(request.referrer)
    else:
        affected_rows = AdminModel().validado_profesor_grupo(id)
        if affected_rows == 1:
            print("Tu datos ha sido guardado.")
            return redirect(request.referrer)
        else:
            print("Algo Salio Mal")
            return redirect(request.referrer)



# ALUMNOS

@admin_bp.route('/add_alumno', methods=['POST', 'GET'])
def add_alumno():
    if request.method == 'POST':
        datos_alumno = add_form()
        affected_rows = AdminModel().add_alumno(datos_alumno)
        if affected_rows == 1:
            flash("Tu datos ha sido guardado.")
            return redirect(url_for("admin.alumnos_admin")) 
        else:
            print("Algo Salio Mal")
            return redirect(url_for("admin.alumnos_admin")) 
    else :
        return redirect(url_for("admin.alumnos_admin")) 

@admin_bp.route('/delete/alumno/<id>')
def delete_alumno(id):
    affected_rows = AdminModel().delete_alumno(id)
    if affected_rows == 1:
        flash("EL dato fue borrado")
        return redirect(url_for("admin.alumnos_admin")) 
    else:
        print("Algo Salio Mal")
        return redirect(url_for("admin.alumnos_admin")) 


@admin_bp.route('/updata/alumno/<id>', methods=['POST', 'GET'])
def updata_alumno(id):
    if request.method == 'POST':
        datos_alumno = add_form()
        affected_rows = AdminModel().update_alumno(datos_alumno, id)
        if affected_rows == 1:
            flash("Tu datos ha sido Actualizado.")
            return redirect(url_for("admin.alumnos_admin")) 
        else:
            print("Algo Salio Mal")
            return redirect(url_for("admin.alumnos_admin")) 
    else :
        return redirect(url_for("admin.alumnos_admin")) 
  

@admin_bp.route('/alumnos')
@admin_required
def alumnos_admin():
    datos = AdminModel().views_alumnos()
    return render_template('/admin/alumnos.html', datos=datos)

@admin_bp.route('/alumno/clases/<id>')
def alumno_view_infor(id):
    datos = AdminModel.viws_clases_alumno(id)
    return render_template("/admin/view-tabla/alumno-dato.html", datos=datos)
    
@admin_bp.route('/alumno/clases/borra/<id>')
def borra_clase_alumno(id):
    affected_rows = AdminModel().delete_clases_alumno(id)
    if affected_rows == 1:
        print("Tu datos ha sido guardado.")
        return redirect(request.referrer)
    else:
        print("Algo Salio Mal")
        return redirect(request.referrer)




# GRUPOS

@admin_bp.route('/add_grupo', methods=['POST', 'GET'])
def add_grupo():
    if request.method == 'POST':
        datos_grupo = add_form()
        affected_rows = AdminModel().add_grupo(datos_grupo)
        if affected_rows == 1:
            flash("Tu datos ha sido guardado.")
            return redirect(url_for("admin.grupos_admin")) 
        else:
            print("Algo Salio Mal")
            return redirect(url_for("admin.grupos_admin")) 
    else :
        return redirect(url_for("admin.grupos_admin")) 


@admin_bp.route('/delete/grupo/<id>')
def delete_grupo(id):
    affected_rows = AdminModel().delete_grupo(id)
    if affected_rows == 1:
        flash("EL dato fue borrado")
        return redirect(url_for("admin.grupos_admin")) 
    else:
        print("Algo Salio Mal")
        return redirect(url_for("admin.grupos_admin")) 


@admin_bp.route('/updata/grupo/<id>', methods=['POST', 'GET'])
def updata_grupo(id):
    if request.method == 'POST':
        datos_grupo = add_form()
        affected_rows = AdminModel().update_grupo(datos_grupo, id)
        if affected_rows == 1:
            flash("Tu datos ha sido Actualizado.")
            return redirect(url_for("admin.grupos_admin")) 
        else:
            print("Algo Salio Mal")
            return redirect(url_for("admin.grupos_admin")) 
    else :
        return redirect(url_for("admin.grupos_admin")) 
  

@admin_bp.route('/grupos')
@admin_required
def grupos_admin():
    datos = AdminModel().views_grupos()
    return render_template('/admin/grupos.html', datos=datos)


@admin_bp.route('/grupo/clases/<id>')
def grupo_view_infor(id):
    datos = AdminModel.viws_clases_grupo(id)
    return render_template("/admin/view-tabla/grupo-dato.html", datos=datos)


@admin_bp.route('/grupo/clases/borra/<id>')
def borra_clase_grupo(id):
    affected_rows = AdminModel().delete_clases_grupo(id)
    if affected_rows == 1:
        print("Tu datos ha sido guardado.")
        return redirect(request.referrer)
    else:
        print("Algo Salio Mal")
        return redirect(request.referrer)
