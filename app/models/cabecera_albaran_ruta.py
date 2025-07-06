import datetime
from decimal import Decimal, InvalidOperation
from app.models.bd_postgresql import get_postgresql_connection
from app.models.rutas import get_ruta_by_id

def obtener_siguiente_numero_albaran(conn=None, cur=None):
    """
    Obtiene el siguiente número de albarán usando un bloqueo de sesión para evitar duplicados
    en situaciones concurrentes.
    """
    close_connection = False
    if not conn or not cur:
        conn = get_postgresql_connection()
        cur = conn.cursor()
        close_connection = True

    try:
        # Adquirir un bloqueo exclusivo a nivel de sesión
        cur.execute("SELECT pg_advisory_xact_lock(1)")  # 1 es un ID arbitrario para este bloqueo
        
        año_actual = datetime.date.today().year
        
        # Obtener el último número del año actual
        cur.execute("""
            SELECT MAX(CAST(SPLIT_PART(numero_albaran, '/', 2) AS INTEGER))
            FROM cabecera_albaran_ruta
            WHERE numero_albaran LIKE %s
        """, (f"{año_actual}/%",))
        
        row = cur.fetchone()
        siguiente = (row[0] or 0) + 1
        
        # Formatear el nuevo número
        nuevo_numero = f"{año_actual}/{siguiente:03d}"
        
        if close_connection:
            conn.commit()
            
        return nuevo_numero
    except Exception as e:
        if close_connection:
            conn.rollback()
        raise Exception(f"Error al obtener número de albarán: {str(e)}")
    finally:
        if close_connection:
            cur.close()
            conn.close()

def calcular_porcentaje_pactado(ruta_id):
    """Calcula el porcentaje pactado según la ruta"""
    conn = get_postgresql_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT nombre_ruta FROM rutas WHERE id = %s", (ruta_id,))
        row = cur.fetchone()
        if not row:
            return Decimal('5.00')  # porcentaje por defecto
        
        nombre = row[0].upper()
        if nombre in ("SAN FRANCISCO", "MARGEN IZQUIERDA"):
            return Decimal('4.00')
        elif nombre == "PAMPLONA":
            return Decimal('6.00')
        elif nombre == "FRANCIA":
            return Decimal('8.00')
        else:
            return Decimal('5.00')
    finally:
        cur.close()
        conn.close()

def validar_fecha(fecha):
    """Valida que la fecha sea válida y no esté en el futuro"""
    if not isinstance(fecha, datetime.date):
        raise ValueError("La fecha debe ser un objeto date válido")
    
    if fecha > datetime.date.today():
        raise ValueError("La fecha no puede ser futura")
    
    return fecha

def validar_porcentaje(porcentaje):
    """Valida que el porcentaje sea un número válido entre 0 y 100"""
    try:
        if isinstance(porcentaje, str):
            porcentaje = Decimal(porcentaje.replace(',', '.'))
        elif isinstance(porcentaje, (int, float)):
            porcentaje = Decimal(str(porcentaje))
        elif not isinstance(porcentaje, Decimal):
            raise ValueError("Tipo de dato no válido para porcentaje")
        
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        
        return porcentaje.quantize(Decimal('0.01'))
    except InvalidOperation:
        raise ValueError("El porcentaje debe ser un número válido")

def crear_cabecera_albaran_ruta(data):
    """
    Crea una nueva cabecera de albarán.
    Required data keys: fecha, transportista_id, ruta_id, usuario_id
    Optional: porcentaje_pactado (se calcula automáticamente si no se proporciona)
    """
    conn = get_postgresql_connection()
    cur = conn.cursor()
    try:
        # Iniciar transacción
        cur.execute("BEGIN")

        # Validar datos requeridos
        required_fields = ['fecha', 'transportista_id', 'ruta_id', 'usuario_id']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo requerido faltante: {field}")

        # Validar tipos de datos
        data['fecha'] = validar_fecha(data['fecha'])
        data['transportista_id'] = int(data['transportista_id'])
        data['ruta_id'] = int(data['ruta_id'])
        data['usuario_id'] = int(data['usuario_id'])

        # Generar número de albarán dentro de la misma transacción
        if 'numero_albaran' not in data:
            data['numero_albaran'] = obtener_siguiente_numero_albaran(conn, cur)

        # Calcular y validar porcentaje pactado
        if 'porcentaje_pactado' not in data:
            data['porcentaje_pactado'] = calcular_porcentaje_pactado(data['ruta_id'])
        else:
            data['porcentaje_pactado'] = validar_porcentaje(data['porcentaje_pactado'])

        # Inicializar campos numéricos en 0
        numeric_fields = [
            'base_imponible', 'importe_liquido', 'importe_transporte',
            'beneficio', 'beneficio_post_log', 'porcentaje_ben_real',
            'lineas_pedido', 'cantidad_pedidos'
        ]
        for field in numeric_fields:
            if field not in data:
                data[field] = Decimal('0.00')
            elif not isinstance(data[field], Decimal):
                data[field] = Decimal(str(data[field])).quantize(Decimal('0.01'))

        cur.execute("""
            INSERT INTO cabecera_albaran_ruta
                (fecha, transportista_id, ruta_id, base_imponible, importe_liquido, 
                importe_transporte, beneficio, beneficio_post_log, porcentaje_ben_real,
                lineas_pedido, porcentaje_pactado, usuario_id, fecha_registro,
                numero_albaran, cantidad_pedidos)
            VALUES
                (%(fecha)s, %(transportista_id)s, %(ruta_id)s, %(base_imponible)s,
                %(importe_liquido)s, %(importe_transporte)s, %(beneficio)s,
                %(beneficio_post_log)s, %(porcentaje_ben_real)s, %(lineas_pedido)s,
                %(porcentaje_pactado)s, %(usuario_id)s, now(), %(numero_albaran)s,
                %(cantidad_pedidos)s)
                RETURNING id, numero_albaran
        """, data)
            
        result = cur.fetchone()
        conn.commit()
        return {'id': result[0], 'numero_albaran': result[1]}
    
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_cabecera_by_id(cabecera_id):
    """Obtiene una cabecera por su ID"""
    conn = get_postgresql_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT c.*, r.nombre_ruta, 
                   t.nombres || ' ' || t.apellidos as transportista_nombre,
                   u.nickname as usuario_nombre
            FROM cabecera_albaran_ruta c
            JOIN rutas r ON c.ruta_id = r.id
            JOIN transportistas t ON c.transportista_id = t.id
            JOIN usuarios u ON c.usuario_id = u.id
            WHERE c.id = %s
        """, (cabecera_id,))
        row = cur.fetchone()
        if row:
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))
        return None
    finally:
        cur.close()
        conn.close()

def actualizar_cabecera(cabecera_id, data):
    """
    Actualiza una cabecera existente.
    Solo permite actualizar campos específicos antes de tener líneas.
    """
    conn = get_postgresql_connection()
    cur = conn.cursor()
    try:
        # Verificar si tiene líneas
        cur.execute("SELECT lineas_pedido FROM cabecera_albaran_ruta WHERE id = %s", (cabecera_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Cabecera no encontrada")
        
        tiene_lineas = row[0] > 0

        # Campos permitidos para actualizar
        allowed_fields = ['fecha', 'transportista_id', 'ruta_id', 'porcentaje_pactado']
        if tiene_lineas:
            allowed_fields = ['fecha']  # Si tiene líneas, solo permite cambiar la fecha

        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        if not update_data:
            return False

        # Construir query de actualización
        set_clause = ", ".join(f"{k} = %({k})s" for k in update_data.keys())
        update_data['id'] = cabecera_id

        cur.execute(f"""
            UPDATE cabecera_albaran_ruta
            SET {set_clause}
            WHERE id = %(id)s
        """, update_data)
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_rutas():
    """Obtiene lista de rutas activas"""
    conn = get_postgresql_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, nombre_ruta as nombre, 
                   CASE 
                       WHEN UPPER(nombre_ruta) IN ('SAN FRANCISCO', 'MARGEN IZQUIERDA') THEN 4.00
                       WHEN UPPER(nombre_ruta) = 'PAMPLONA' THEN 6.00
                       WHEN UPPER(nombre_ruta) = 'FRANCIA' THEN 8.00
                       ELSE 5.00
                   END as porcentaje_default
            FROM rutas 
            WHERE activo = true
            ORDER BY nombre_ruta
        """)
        rutas = []
        for row in cur.fetchall():
            rutas.append({
                'id': row[0],
                'nombre': row[1],
                'porcentaje_default': row[2]
            })
        return rutas
    finally:
        cur.close()
        conn.close()

def get_transportistas():
    """Obtiene lista de transportistas activos"""
    conn = get_postgresql_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, nombres || ' ' || apellidos as nombre, telefono
            FROM transportistas 
            WHERE activo = true
            ORDER BY nombres, apellidos
        """)
        transportistas = []
        for row in cur.fetchall():
            transportistas.append({
                'id': row[0],
                'nombre': row[1],
                'telefono': row[2]
            })
        return transportistas
    finally:
        cur.close()
        conn.close()
