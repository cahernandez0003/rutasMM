from flask import Blueprint, render_template

albaranes_rutas_bp = Blueprint('albaranes', __name__, template_folder='../templates/pages')

@albaranes_rutas_bp.route('/')
def index():
    return render_template('pages/albaranes.html', title='Albaranes de rutas')
