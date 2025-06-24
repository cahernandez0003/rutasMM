from app.models.bd_postgresql import get_postgresql_connection

def get_all_rutas():
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rutas ORDER BY id DESC;")
    columns = [desc[0] for desc in cur.description]
    rutas = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return rutas

def get_ruta_by_id(ruta_id):
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rutas WHERE id = %s;", (ruta_id,))
    columns = [desc[0] for desc in cur.description]
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return dict(zip(columns, row))
    return None

def create_ruta(codigo_ruta, nombre_ruta):
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO rutas (codigo_ruta, nombre_ruta) VALUES (%s, %s) RETURNING id;",
        (codigo_ruta, nombre_ruta)
    )
    ruta_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return ruta_id

def update_ruta(ruta_id, codigo_ruta, nombre_ruta, activo):
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE rutas SET codigo_ruta=%s, nombre_ruta=%s, activo=%s WHERE id=%s;",
        (codigo_ruta, nombre_ruta, activo, ruta_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_ruta(ruta_id):
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM rutas WHERE id=%s;", (ruta_id,))
    conn.commit()
    cur.close()
    conn.close()
