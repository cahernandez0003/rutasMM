from flask import Flask, render_template
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    from app.routes.rutas import rutas_bp
    from app.routes.transportistas import transportistas_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.auth import auth_bp
    from app.routes.albaranes import albaranes_bp

    app.register_blueprint(rutas_bp, url_prefix='/rutas')
    app.register_blueprint(transportistas_bp, url_prefix='/transportistas')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(albaranes_bp, url_prefix='/albaranes_rutas')
    app.register_blueprint(auth_bp)

    app.secret_key = app.config.get('SECRET_KEY', '10256535')

    @app.context_processor
    def inject_globals():
        return {
            'year': datetime.now().year,
            'app_name': 'Sistema de Gestión de Rutas'
        }

    @app.route('/')
    def home():
        return render_template('pages/home.html', title='Inicio')

    @app.errorhandler(404)
    def not_found(error):
        return render_template('pages/error.html', 
                             error_code=404,
                             error_message="Página no encontrada"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('pages/error.html',
                             error_code=500,
                             error_message="Error interno del servidor"), 500

    return app
