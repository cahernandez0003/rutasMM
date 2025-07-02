from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.usuarios import (
    get_all_usuarios, get_usuario_by_id,
    create_usuario, update_usuario, delete_usuario
)
from werkzeug.security import generate_password_hash
from app.decorators import requiere_login, requiere_rol

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/')
@requiere_login
@requiere_rol('supus', 'admin')
def index():
    usuarios = get_all_usuarios()
    return render_template('pages/usuarios/index.html', usuarios=usuarios, title="Usuarios")

@usuarios_bp.route('/crear', methods=['GET', 'POST'])
@requiere_login
@requiere_rol('supus', 'admin')
def crear():
    if request.method == 'POST':
        data = {
            'nombres': request.form.get('nombres'),
            'apellidos': request.form.get('apellidos'),
            'nickname': request.form.get('nickname'),
            'password_hash': generate_password_hash(request.form.get('password')),
            'requiere_cambio_pw': 'requiere_cambio_pw' in request.form,
            'email': request.form.get('email'),
            'rol': request.form.get('rol')
        }
        try:
            create_usuario(data)
            flash('Usuario creado con éxito.', 'success')
            return redirect(url_for('usuarios.index'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('pages/usuarios/form.html', action="Crear", u=None)

@usuarios_bp.route('/editar/<int:usuario_id>', methods=['GET', 'POST'])
@requiere_login
@requiere_rol('supus', 'admin')
def editar(usuario_id):
    u = get_usuario_by_id(usuario_id)
    if not u:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('usuarios.index'))
    if request.method == 'POST':
        data = {
            'nombres': request.form.get('nombres'),
            'apellidos': request.form.get('apellidos'),
            'nickname': request.form.get('nickname'),
            'password_hash': u['password_hash'] if not request.form.get('password') else generate_password_hash(request.form.get('password')),
            'requiere_cambio_pw': 'requiere_cambio_pw' in request.form,
            'email': request.form.get('email'),
            'rol': request.form.get('rol'),
            'activo': 'activo' in request.form
        }
        try:
            update_usuario(usuario_id, data)
            flash('Usuario actualizado.', 'success')
            return redirect(url_for('usuarios.index'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('pages/usuarios/form.html', action="Editar", u=u)

@usuarios_bp.route('/eliminar/<int:usuario_id>', methods=['POST'])
@requiere_login
@requiere_rol('supus', 'admin')
def eliminar(usuario_id):
    try:
        delete_usuario(usuario_id)
        flash('Usuario eliminado.', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('usuarios.index'))