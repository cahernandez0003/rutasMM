from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Importa blueprints aquí dentro de la función, no arriba
    from app.routes.rutas import rutas_bp
    from app.routes.transportistas import transportistas_bp

    # Registra blueprints aquí, usando la variable local 'app'
    app.register_blueprint(rutas_bp, url_prefix='/rutas')
    app.register_blueprint(transportistas_bp, url_prefix='/transportistas')

    # ...otros registros o configuraciones

    return app
