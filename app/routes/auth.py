from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from app.models.usuarios import get_usuario_by_nickname
from app.models.logins import registrar_login

auth_bp = Blueprint('auth', __name__, template_folder='../templates/pages/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']
        usuario = get_usuario_by_nickname(nickname)
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        if usuario and check_password_hash(usuario['password_hash'], password):
            # Login exitoso
            registrar_login(usuario['id'], ip_address, user_agent, exito=True)
            session['usuario_id'] = usuario['id']
            session['usuario_rol'] = usuario['rol']
            session['usuario_nickname'] = usuario['nickname']
            flash(f"Bienvenido, {usuario['nombres']}")
            return redirect(url_for('home'))
        else:
            # Login fallido
            if usuario:
                registrar_login(usuario['id'], ip_address, user_agent, exito=False, observaciones="Contraseña incorrecta")
            flash("Usuario o contraseña incorrectos", "danger")
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for('auth.login'))
