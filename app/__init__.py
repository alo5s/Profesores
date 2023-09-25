from flask import Flask, session, redirect, request, url_for
# Impor la config
from config import Config, DevelopmentConfig
# Import la routes
from .routes import home_bp, clases_bp, alumnos_bp, usuario_bp, admin_bp

app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)
app.config.from_object(DevelopmentConfig)


app.register_blueprint(home_bp)
app.register_blueprint(clases_bp)
app.register_blueprint(alumnos_bp)

# Rutas protegidas en los blueprints login usario
app.register_blueprint(usuario_bp)
# Ruta admino 
app.register_blueprint(admin_bp)


# Rutas ingreso a usario normal
protected_routes_usario = ['home.home', "clases.clases", "alumnos.alumnos"]

@app.before_request
def before_request():
    app.logger.debug(f"Endpoint: {request.endpoint}, Username in session: {'username' in session}")
    if request.endpoint in protected_routes_usario and 'username' not in session:
        app.logger.debug("Redirecting to login page")
        return redirect(url_for('usuario.login')) 
