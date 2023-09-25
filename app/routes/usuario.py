from flask import Blueprint, render_template, request, redirect, session, url_for

# Models
from ..models.UsuarioModels import UsuarioModel

usuario_bp = Blueprint('usuario',__name__)

@usuario_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_model = UsuarioModel()
        user = user_model.get_usuario_por_nombre(username)
        print(user)
        if user and user['contraseña'] == password:
            session['id'] = user["id"] 
            session['username'] = user['fullname']
            print(session)  
            return redirect(url_for("home.home")) 
        return "Credenciales inválidas" 
    else:
        return render_template("login.html")
    

@usuario_bp.route("/logout")
def logout():
    session.pop('username', None)  # Elimina el nombre de usuario de la sesión
    return redirect("/")
