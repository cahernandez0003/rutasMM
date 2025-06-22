from flask import Blueprint, render_template

transportistas_bp = Blueprint('transportistas', __name__, template_folder='../templates/pages')

@transportistas_bp.route('/')
def index():
    return render_template('pages/home.html', title='Transportistas')
