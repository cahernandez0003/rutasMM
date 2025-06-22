from flask import Blueprint, render_template

usuarios_bp = Blueprint('usuarios', __name__, template_folder='../templates/pages')

@usuarios_bp.route('/')
def index():
    return render_template('pages/home.html', title='Usuarios')
