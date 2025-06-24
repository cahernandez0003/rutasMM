from app.models.bd_postgresql import get_postgresql_connection

def get_all_transportistas():
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transportistas ORDER BY id DESC;")
    columns = [desc[0] for desc in cur.description]
    items = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return items

def get_transportista_by_id(transportista_id):
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transportistas WHERE id = %s;", (transportista_id,))
    columns = [desc[0] for desc in cur.description]
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return dict(zip(columns, row))
    return None

def create_transportista(data):
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO transportistas
        (nombres, apellidos, telefono, direccion, email, documento_cif, codigo_postal)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """, (
            data['nombres'], data['apellidos'], data['telefono'], data['direccion'],
            data['email'], data['documento_cif'], data['codigo_postal']
        )
    )
    tid = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return tid

def update_transportista(transportista_id, data):
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE transportistas
        SET nombres=%s, apellidos=%s, telefono=%s, direccion=%s, email=%s,
            documento_cif=%s, codigo_postal=%s, activo=%s
        WHERE id=%s;
        """, (
            data['nombres'], data['apellidos'], data['telefono'], data['direccion'],
            data['email'], data['documento_cif'], data['codigo_postal'], data['activo'],
            transportista_id
        )
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_transportista(transportista_id):
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM transportistas WHERE id=%s;", (transportista_id,))
    conn.commit()
    cur.close()
    conn.close()
