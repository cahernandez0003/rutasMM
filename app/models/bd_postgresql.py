import psycopg2

def get_postgresql_connection():
    try:
        return psycopg2.connect(
            host="localhost",        # Cambia si tu BD está en otro lado
            port=5432,               # Puerto de PostgreSQL
            database="logistica_rutas",  # Tu base de datos real
            user="postgres",          # Tu usuario
            password="091123"      # Tu contraseña
        )
    except Exception as e:
        print(f"Error de conexión a PostgreSQL: {e}")
        return None
