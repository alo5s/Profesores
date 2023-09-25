from flask import Blueprint, render_template, session

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if 'username' in session:
        id_usuario = session['username']
        #seguimiento_datos = SegumientoModel.get_favoritos(id_usuario)
    else:
        seguimiento_datos = []
    return render_template('home.html')
