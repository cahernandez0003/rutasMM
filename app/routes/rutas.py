from flask import Blueprint, render_template

rutas_bp = Blueprint('rutas', __name__, template_folder='../templates/pages')

@rutas_bp.route('/')
def index():
    return render_template('pages/home.html', title='Rutas')
