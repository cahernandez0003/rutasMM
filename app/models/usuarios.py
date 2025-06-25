from app.models.bd_postgresql import get_postgresql_connection

def get_all_usuarios():
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios ORDER BY id DESC;")
    columns = [desc[0] for desc in cur.description]
    items = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return items

def get_usuario_by_id(usuario_id):
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = %s;", (usuario_id,))
    columns = [desc[0] for desc in cur.description]
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return dict(zip(columns, row))
    return None

def create_usuario(data):
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO usuarios
        (nombres, apellidos, nickname, password_hash, requiere_cambio_pw, email, rol)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """, (
            data['nombres'], data['apellidos'], data['nickname'],
            data['password_hash'], data['requiere_cambio_pw'],
            data['email'], data['rol']
        )
    )
    uid = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return uid

def update_usuario(usuario_id, data):
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE usuarios
        SET nombres=%s, apellidos=%s, nickname=%s, password_hash=%s,
            requiere_cambio_pw=%s, email=%s, rol=%s, activo=%s
        WHERE id=%s;
        """, (
            data['nombres'], data['apellidos'], data['nickname'],
            data['password_hash'], data['requiere_cambio_pw'],
            data['email'], data['rol'], data['activo'],
            usuario_id
        )
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_usuario(usuario_id):
    conn = get_postgresql_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuarios WHERE id=%s;", (usuario_id,))
    conn.commit()
    cur.close()
    conn.close()