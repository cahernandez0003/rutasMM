from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.rutas import get_all_rutas, get_ruta_by_id, create_ruta, update_ruta, delete_ruta
from app.decorators import requiere_login, requiere_rol

rutas_bp = Blueprint('rutas', __name__)

@rutas_bp.route('/')
@requiere_login
@requiere_rol('supus', 'admin')
def index():
    rutas = get_all_rutas()
    return render_template('pages/rutas/index.html', rutas=rutas, title="Rutas")

@rutas_bp.route('/crear', methods=['GET', 'POST'])
@requiere_login
@requiere_rol('supus', 'admin')
def crear():
    if request.method == 'POST':
        codigo = request.form['codigo_ruta']
        nombre = request.form['nombre_ruta']
        try:
            create_ruta(codigo, nombre)
            flash('Ruta creada con éxito.', 'success')
            return redirect(url_for('rutas.index'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('pages/rutas/form.html', action="Crear", ruta=None)

@rutas_bp.route('/editar/<int:ruta_id>', methods=['GET', 'POST'])
@requiere_login
@requiere_rol('supus', 'admin')
def editar(ruta_id):
    ruta = get_ruta_by_id(ruta_id)
    if not ruta:
        flash('Ruta no encontrada.', 'danger')
        return redirect(url_for('rutas.index'))
    if request.method == 'POST':
        codigo = request.form['codigo_ruta']
        nombre = request.form['nombre_ruta']
        activo = 'activo' in request.form
        try:
            update_ruta(ruta_id, codigo, nombre, activo)
            flash('Ruta actualizada con éxito.', 'success')
            return redirect(url_for('rutas.index'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('pages/rutas/form.html', action="Editar", ruta=ruta)

@rutas_bp.route('/eliminar/<int:ruta_id>', methods=['POST'])
@requiere_login
@requiere_rol('supus', 'admin')
def eliminar(ruta_id):
    try:
        delete_ruta(ruta_id)
        flash('Ruta eliminada.', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('rutas.index'))
