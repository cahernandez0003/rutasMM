import datetime
from app.models.bd_postgresql import get_postgresql_connection

def obtener_siguiente_numero_albaran():
    año_actual = datetime.date.today().year
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT numero_albaran
        FROM cabecera_albaran_ruta
        WHERE numero_albaran LIKE %s
        ORDER BY numero_albaran DESC
        LIMIT 1
    """, (f"{año_actual}/%",))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row and row[0]:
        ultimo_numero = int(row[0].split('/')[-1])
        siguiente = ultimo_numero + 1
    else:
        siguiente = 1
    return f"{año_actual}/{siguiente:03d}"

def calcular_porcentaje_pactado(nombre_ruta):
    nombre = nombre_ruta.upper()
    if nombre in ("SAN FRANCISCO", "MARGEN IZQUIERDA"):
        return 4.0
    elif nombre == "PAMPLONA":
        return 6.0
    else:
        return 5.0

def crear_cabecera_albaran_ruta(data):
    # data es un dict con los campos necesarios
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO cabecera_albaran_ruta
        (fecha, transportista_id, ruta_id, base_imponible, importe_liquido, importe_transporte,
         beneficio, beneficio_post_log, porcentaje_ben_real, lineas_pedido, porcentaje_pactado,
         usuario_id, fecha_registro, numero_albaran, cantidad_pedidos)
        VALUES
        (%(fecha)s, %(transportista_id)s, %(ruta_id)s, %(base_imponible)s, %(importe_liquido)s, %(importe_transporte)s,
         %(beneficio)s, %(beneficio_post_log)s, %(porcentaje_ben_real)s, %(lineas_pedido)s, %(porcentaje_pactado)s,
         %(usuario_id)s, now(), %(numero_albaran)s, %(cantidad_pedidos)s)
        RETURNING id
    """, data)
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id

def get_rutas():  # Helper para combos
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre_ruta FROM rutas WHERE activo = true ORDER BY nombre_ruta;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_transportistas():
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombres || ' ' || apellidos as nombre FROM transportistas WHERE activo = true ORDER BY nombre;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
