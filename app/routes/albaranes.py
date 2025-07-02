import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.cabecera_albaran_ruta import (
    obtener_siguiente_numero_albaran,
    calcular_porcentaje_pactado,
    crear_cabecera_albaran_ruta,    # nombre correcto según tu modelo
    get_rutas,
    get_transportistas
)
from app.decorators import requiere_login, requiere_rol

albaranes_bp = Blueprint('albaranes', __name__, url_prefix='/albaranes')

@albaranes_bp.route('/')
@requiere_login
@requiere_rol('supus', 'admin')
def index():
    # TODO: Implementar listado de albaranes
    return render_template('albaranes/index.html', title="Albaranes")

@albaranes_bp.route('/nuevo', methods=['GET', 'POST'])
@requiere_login
@requiere_rol('supus', 'admin')
def nuevo():
    rutas = get_rutas()
    transportistas = get_transportistas()
    fecha_hoy = datetime.date.today().strftime('%Y-%m-%d')
    if request.method == 'POST':
        data = request.form.to_dict()
        # Consigue el nombre de la ruta para calcular % pactado
        ruta_nombre = next((n for i, n in rutas if str(i) == data['ruta_id']), None)
        data['porcentaje_pactado'] = request.form.get('porcentaje_pactado') or calcular_porcentaje_pactado(ruta_nombre)
        data['numero_albaran'] = obtener_siguiente_numero_albaran()
        data['usuario_id'] = session['usuario_id']
        # Base imponible debe llegar como número (cast)
        data['base_imponible'] = float(data['base_imponible'])
        cab_id = crear_cabecera_albaran_ruta(data)
        flash("Cabecera creada correctamente. Puedes continuar con las líneas.", "success")
        # Redirige a la pantalla de agregar líneas, si la tienes, o muestra resumen
        # (Debes crear la función/ver template 'ver' luego)
        return redirect(url_for('albaranes.index'))
    return render_template(
        'albaranes/form.html',
        rutas=rutas,
        transportistas=transportistas,
        fecha_hoy=fecha_hoy
    )
