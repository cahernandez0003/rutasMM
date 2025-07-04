from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    from app.routes.rutas import rutas_bp
    from app.routes.transportistas import transportistas_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.albaranes import albaranes_rutas_bp
    from app.routes.auth import auth_bp





    app.register_blueprint(rutas_bp, url_prefix='/rutas')
    app.register_blueprint(transportistas_bp, url_prefix='/transportistas')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(albaranes_rutas_bp, url_prefix='/albaranes_rutas')
    app.register_blueprint(auth_bp)

    app.secret_key = "10256535"



    @app.route('/')
    def home():
        return render_template('pages/home.html')

    @app.errorhandler(404)
    def not_found(error):
        return "Página no encontrada", 404

    return app
