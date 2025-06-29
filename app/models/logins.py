from app.models.bd_postgresql import get_postgresql_connection

def registrar_login(usuario_id, ip_address, user_agent, exito=True, observaciones=None):
    """
    Registra un intento de login y actualiza el campo last_login en usuarios si fue exitoso.
    """
    conn = get_postgresql_connection()
    cur = conn.cursor()
    # Insertar el login
    cur.execute("""
        INSERT INTO logins (usuario_id, ip_address, user_agent, exito, observaciones)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING login_timestamp;
    """, (usuario_id, ip_address, user_agent, exito, observaciones))
    login_time = cur.fetchone()[0]
    # Si fue exitoso, actualizar last_login en usuarios
    if exito:
        cur.execute("""
            UPDATE usuarios SET last_login = %s WHERE id = %s;
        """, (login_time, usuario_id))
    conn.commit()
    cur.close()
    conn.close()
