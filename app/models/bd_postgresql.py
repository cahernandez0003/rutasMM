import psycopg2
from psycopg2.extras import DictCursor

class BDPostgresql:
    def __init__(self):
        self.conn = None
        self.cur = None

    def conectar(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",        # Cambia si tu BD está en otro lado
                port=5432,               # Puerto de PostgreSQL
                database="logistica_rutas",  # Tu base de datos real
                user="postgres",          # Tu usuario
                password="091123"      # Tu contraseña
            )
            self.cur = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Error de conexión a PostgreSQL: {e}")
            return False

    def ejecutar_sql(self, sql, valores=None):
        try:
            if not self.conn or not self.cur:
                if not self.conectar():
                    raise Exception("No se pudo establecer la conexión")
            
            self.cur.execute(sql, valores)
            
            # Si es un SELECT, retornar resultados
            if sql.strip().upper().startswith('SELECT'):
                return self.cur.fetchall()
            
            # Si es INSERT y tiene RETURNING, retornar el resultado
            elif sql.strip().upper().startswith('INSERT') and 'RETURNING' in sql.upper():
                return self.cur.fetchone()
            
            # Para otros casos (UPDATE, DELETE, etc.)
            self.conn.commit()
            return True
            
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            raise Exception(f"Error ejecutando SQL: {str(e)}")
        
    def cerrar(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def __del__(self):
        self.cerrar()

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
