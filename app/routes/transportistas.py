from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.transportistas import (
    get_all_transportistas, get_transportista_by_id,
    create_transportista, update_transportista, delete_transportista
)
from app.decorators import requiere_login, requiere_rol

transportistas_bp = Blueprint('transportistas', __name__)

@transportistas_bp.route('/')
@requiere_login
@requiere_rol('supus', 'admin')
def index():
    transportistas = get_all_transportistas()
    return render_template('pages/transportistas/index.html', transportistas=transportistas, title="Transportistas")

@transportistas_bp.route('/crear', methods=['GET', 'POST'])
@requiere_login
@requiere_rol('supus', 'admin')
def crear():
    if request.method == 'POST':
        data = {k: request.form.get(k) for k in
            ['nombres', 'apellidos', 'telefono', 'direccion', 'email', 'documento_cif', 'codigo_postal']
        }
        try:
            create_transportista(data)
            flash('Transportista creado con éxito.', 'success')
            return redirect(url_for('transportistas.index'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('pages/transportistas/form.html', action="Crear", t=None)

@transportistas_bp.route('/editar/<int:transportista_id>', methods=['GET', 'POST'])
@requiere_login
@requiere_rol('supus', 'admin')
def editar(transportista_id):
    t = get_transportista_by_id(transportista_id)
    if not t:
        flash('Transportista no encontrado.', 'danger')
        return redirect(url_for('transportistas.index'))
    if request.method == 'POST':
        data = {k: request.form.get(k) for k in
            ['nombres', 'apellidos', 'telefono', 'direccion', 'email', 'documento_cif', 'codigo_postal']
        }
        data['activo'] = 'activo' in request.form
        try:
            update_transportista(transportista_id, data)
            flash('Transportista actualizado.', 'success')
            return redirect(url_for('transportistas.index'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('pages/transportistas/form.html', action="Editar", t=t)

@transportistas_bp.route('/eliminar/<int:transportista_id>', methods=['POST'])
@requiere_login
@requiere_rol('supus', 'admin')
def eliminar(transportista_id):
    try:
        delete_transportista(transportista_id)
        flash('Transportista eliminado.', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('transportistas.index'))
