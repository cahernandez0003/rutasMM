import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.models.cabecera_albaran_ruta import (
    crear_cabecera_albaran_ruta, get_rutas, get_transportistas,
    obtener_siguiente_numero_albaran, get_cabecera_by_id
)
from app.models.transportistas import get_transportista_by_id
from app.decorators import requiere_login, requiere_rol
from app.utils.postal_codes import get_location_info

albaranes_bp = Blueprint('albaranes', __name__)

@albaranes_bp.route('/api/transportista/<int:transportista_id>')
@requiere_login
def get_transportista_data(transportista_id):
    transportista = get_transportista_by_id(transportista_id)
    if not transportista:
        return jsonify({'error': 'Transportista no encontrado'}), 404
    
    # Obtener información de ubicación basada en el código postal
    if 'codigo_postal' in transportista:
        location_info = get_location_info(transportista['codigo_postal'])
        transportista['provincia'] = location_info['provincia']
        transportista['municipio'] = location_info['provincia']  # Usamos la provincia como municipio por ahora
    
    return jsonify(transportista)

@albaranes_bp.route('/api/siguiente_numero')
@requiere_login
def get_siguiente_numero():
    try:
        numero = obtener_siguiente_numero_albaran()
        return jsonify({'numero': numero})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@albaranes_bp.route('/')
@requiere_login
@requiere_rol('supus', 'admin')
def index():
    return render_template('albaranes/index.html', title="Albaranes")

@albaranes_bp.route('/nuevo', methods=['GET', 'POST'])
@requiere_login
@requiere_rol('supus', 'admin')
def nuevo():
    if request.method == 'POST':
        try:
            # Verificar si es una petición AJAX
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            # Obtener y validar datos
            data = {
                'fecha': datetime.datetime.strptime(request.form['fecha'], '%Y-%m-%d').date(),
                'transportista_id': int(request.form['transportista_id']),
                'ruta_id': int(request.form['ruta_id']),
                'porcentaje_pactado': float(request.form['porcentaje_pactado']),
                'usuario_id': session.get('usuario_id')
            }
            
            if not data['usuario_id']:
                if is_ajax:
                    return jsonify({
                        'success': False,
                        'message': 'Sesión no válida. Por favor, inicie sesión nuevamente.'
                    }), 401
                flash('Sesión no válida. Por favor, inicie sesión nuevamente.', 'danger')
                return redirect(url_for('auth.login'))

            # Obtener el siguiente número de albarán
            try:
                data['numero_albaran'] = obtener_siguiente_numero_albaran()
            except Exception as e:
                if is_ajax:
                    return jsonify({
                        'success': False,
                        'message': f'Error al generar número de albarán: {str(e)}'
                    }), 500
                flash(f'Error al generar número de albarán: {str(e)}', 'danger')
                return redirect(url_for('albaranes.nuevo'))
            
            # Crear el albarán
            result = crear_cabecera_albaran_ruta(data)
            
            if is_ajax:
                return jsonify({
                    'success': True,
                    'message': f'Albarán {result["numero_albaran"]} creado con éxito.',
                    'albaran_id': result['id'],
                    'numero_albaran': result['numero_albaran']
                })
            
            flash(f'Albarán {result["numero_albaran"]} creado con éxito.', 'success')
            return redirect(url_for('albaranes.index'))
            
        except ValueError as e:
            if is_ajax:
                return jsonify({
                    'success': False,
                    'message': f'Error de validación: {str(e)}'
                }), 400
            flash(f'Error de validación: {str(e)}', 'danger')
            return redirect(url_for('albaranes.nuevo'))
        except Exception as e:
            if is_ajax:
                return jsonify({
                    'success': False,
                    'message': f'Error al crear albarán: {str(e)}'
                }), 500
            flash(f'Error al crear albarán: {str(e)}', 'danger')
            return redirect(url_for('albaranes.nuevo'))
    
    # Para peticiones GET, intentar obtener el siguiente número de albarán
    try:
        siguiente_numero = obtener_siguiente_numero_albaran()
    except:
        siguiente_numero = ''
    
    return render_template('albaranes/form.html',
                         rutas=get_rutas(),
                         transportistas=get_transportistas(),
                         fecha_hoy=datetime.date.today().strftime('%Y-%m-%d'),
                         siguiente_numero=siguiente_numero)
