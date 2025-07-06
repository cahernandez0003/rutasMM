import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.models.cabecera_albaran_ruta import (
    crear_cabecera_albaran_ruta, get_rutas, get_transportistas,
    obtener_siguiente_numero_albaran, get_cabecera_by_id
)
from app.models.transportistas import get_transportista_by_id
from app.models.lineas_albaran_ruta import LineasAlbaranRuta
from app.decorators import requiere_login, requiere_rol
from app.utils.postal_codes import get_location_info
from app.models.bd_sqlserver import BDSqlServer

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

@albaranes_bp.route('/api/lineas_ruta/<int:ruta_id>')
@requiere_login
def get_lineas_ruta(ruta_id):
    try:
        lineas = LineasAlbaranRuta.obtener_lineas_por_ruta(ruta_id)
        
        # Transformar los resultados en una lista de diccionarios
        resultados = []
        for linea in lineas:
            resultados.append({
                'numero_albaran': linea[0],
                'nombre_cliente': linea[1],
                'cod_cliente': linea[2],
                'municipio_envio': linea[3],
                'importe': float(linea[4]) if linea[4] else 0.0,
                'beneficio': float(linea[5]) if linea[5] else 0.0,
                'imp_liqu': float(linea[6]) if linea[6] else 0.0,
                'porcentaje': float(linea[7]) if linea[7] else 0.0,
                'conductor': linea[8]
            })
        
        if not resultados:
            return jsonify({
                'success': False,
                'message': 'No se encontraron líneas para esta ruta en la fecha actual'
            }), 404
            
        return jsonify({
            'success': True,
            'data': resultados
        })
    except Exception as e:
        print(f"Error en get_lineas_ruta: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error al cargar líneas de la ruta: {str(e)}'
        }), 500

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
                # En lugar de redirigir, devolvemos los datos necesarios para mostrar las líneas
                return jsonify({
                    'success': True,
                    'message': f'Albarán {result["numero_albaran"]} creado con éxito.',
                    'albaran_id': result['id'],
                    'numero_albaran': result['numero_albaran'],
                    'ruta_id': data['ruta_id'],
                    'porcentaje_pactado': data['porcentaje_pactado']
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

@albaranes_bp.route('/api/buscar_albaran/<serie>/<numero>')
@requiere_login
def buscar_albaran(serie, numero):
    try:
        bd = BDSqlServer()
        sql = """
        SELECT 
            CONCAT(a.SerieAlbaran, a.NumeroAlbaran) AS ALBARAN,
            a.RazonSocial,
            a.CodigoCliente,
            a.MunicipioEnvios,
            a.ImporteLiquido,
            a.FechaAlbaran,
            a.MargenBeneficio,
            a.PorMargenBeneficio,
            t.Transportista,
            a.BaseImponible,
            a.NumeroLineas,
            deuda_table.deuda
        FROM [MMARKET].[dbo].[CabeceraAlbaranCliente] a
        LEFT JOIN Transportistas t 
            ON t.CodigoEmpresa = a.CodigoEmpresa 
            AND t.CodigoTransportista = a.CodigoTransportistaEnvios
        LEFT JOIN (
            SELECT 
                CodigoClienteProveedor,
                CONCAT(FORMAT(SUM(ImporteEfecto), 'N2', 'es-ES'), '€') AS deuda
            FROM CarteraEfectos
            WHERE CodigoEmpresa = 1
                AND Prevision = 'C'
                AND StatusBorrado = 0
            GROUP BY CodigoClienteProveedor
        ) AS deuda_table 
            ON deuda_table.CodigoClienteProveedor = a.CodigoCliente
        WHERE a.CodigoEmpresa = 1
            AND a.Ejercicioalbaran > 2023
            AND a.SerieAlbaran = ?
            AND a.NumeroAlbaran = ?
        """
        
        resultados = bd.ejecutar_sql(sql, (serie, numero))
        
        if not resultados:
            return jsonify({
                'success': False,
                'message': 'No se encontró el albarán'
            }), 404

        resultado = resultados[0]
        
        return jsonify({
            'success': True,
            'data': {
                'fecha_alb': resultado[5].strftime('%Y-%m-%d') if resultado[5] else None,
                'nombre_cliente': resultado[1],
                'cod_cliente': resultado[2],
                'municipio_envio': resultado[3],
                'importe': float(resultado[9]) if resultado[9] else 0,
                'beneficio': float(resultado[6]) if resultado[6] else 0,
                'imp_liqu': float(resultado[4]) if resultado[4] else 0,
                'porcentaje': float(resultado[7]) if resultado[7] else 0,
                'conductor': resultado[8],
                'deuda': resultado[11] if resultado[11] else '0.00€',
                'lineas': int(resultado[10]) if resultado[10] else 0
            }
        })
        
    except Exception as e:
        print(f"Error al buscar albarán: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error al buscar albarán: {str(e)}'
        }), 500
    finally:
        bd.cerrar()
