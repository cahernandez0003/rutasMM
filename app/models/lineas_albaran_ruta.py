from app.models.bd import BD
from app.models.bd_postgresql import BDPostgresql

class LineasAlbaranRuta(BD):
    def __init__(self):
        super().__init__()
        self.id = None
        self.cabecera_id = None  # FK, NOT NULL
        self.fecha_albaran = None
        self.num_alb_ruta = None
        self.serie_alb = None
        self.numero_alb = None
        self.nombre_cliente = None
        self.cod_cliente = None
        self.municipio_envio = None
        self.importe = None
        self.beneficio = None
        self.imp_liqu = None
        self.porcentaje = None
        self.conductor = None
        self.tlpa = None  # Campo calculado: importe * porcentaje
        self.ben_post_log = None  # Campo calculado: beneficio - tlpa
        self.por_ben_real = None  # Campo calculado: ben_post_log / importe
        self.deuda = None
        self.lineas = None
        self.fecha_registro = None  # NOT NULL, default now()

    @staticmethod
    def obtener_lineas_por_ruta(ruta_id):
        bd = BDPostgresql()
        sql = """
        WITH datos_ruta AS (
            SELECT 
                r.id as ruta_id,
                r.nombre_ruta as ruta_nombre,
                t.nombres || ' ' || t.apellidos as transportista_nombre
            FROM rutas r
            LEFT JOIN transportistas t ON r.transportista_id = t.id
            WHERE r.id = %s
        )
        SELECT DISTINCT
            p.numero_albaran,
            p.nombre_cliente,
            p.codigo_cliente as cod_cliente,
            p.municipio_envio,
            p.importe,
            p.beneficio,
            p.importe_liquido as imp_liqu,
            COALESCE(p.porcentaje, 0) as porcentaje,
            dr.transportista_nombre as conductor
        FROM pedidos_sage p
        CROSS JOIN datos_ruta dr
        WHERE p.ruta_id = dr.ruta_id
          AND p.fecha = CURRENT_DATE
        ORDER BY p.numero_albaran;
        """
        try:
            resultados = bd.ejecutar_sql(sql, (ruta_id,))
            return resultados if resultados else []
        except Exception as e:
            print(f"Error en obtener_lineas_por_ruta: {str(e)}")
            return []
        finally:
            bd.cerrar()

    def crear_tabla(self):
        bd = BDPostgresql()
        sql = """
        CREATE TABLE IF NOT EXISTS lineas_albaran_ruta (
            id SERIAL PRIMARY KEY,
            cabecera_id INTEGER REFERENCES cabecera_albaran_ruta(id) NOT NULL,
            fecha_albaran DATE,
            num_alb_ruta TEXT,
            serie_alb TEXT,
            numero_alb TEXT,
            nombre_cliente TEXT,
            cod_cliente TEXT,
            municipio_envio TEXT,
            importe NUMERIC(10,2),
            beneficio NUMERIC(10,2),
            imp_liqu NUMERIC(10,2),
            porcentaje NUMERIC(5,2),
            conductor TEXT,
            tlpa NUMERIC(10,2),
            ben_post_log NUMERIC(10,2),
            por_ben_real NUMERIC(10,2),
            deuda NUMERIC(10,2),
            lineas INTEGER,
            fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            fecha_alb DATE
        );
        """
        try:
            bd.ejecutar_sql(sql)
            print("Tabla lineas_albaran_ruta creada exitosamente")
        except Exception as e:
            print(f"Error al crear tabla lineas_albaran_ruta: {str(e)}")
        finally:
            bd.cerrar()

    def insertar(self):
        bd = BDPostgresql()
        sql = """
        INSERT INTO lineas_albaran_ruta (
            cabecera_id, fecha_albaran, num_alb_ruta, serie_alb, numero_alb,
            nombre_cliente, cod_cliente, municipio_envio, importe, beneficio,
            imp_liqu, porcentaje, conductor, tlpa, ben_post_log, por_ben_real,
            deuda, lineas, fecha_registro, fecha_alb
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) RETURNING id;
        """
        valores = (
            self.cabecera_id, self.fecha_albaran, self.num_alb_ruta,
            self.serie_alb, self.numero_alb, self.nombre_cliente,
            self.cod_cliente, self.municipio_envio, self.importe,
            self.beneficio, self.imp_liqu, self.porcentaje,
            self.conductor, self.tlpa, self.ben_post_log,
            self.por_ben_real, self.deuda, self.lineas,
            self.fecha_registro, self.fecha_alb
        )
        id_insertado = bd.ejecutar_sql(sql, valores)
        return id_insertado

    def actualizar(self):
        bd = BDPostgresql()
        sql = """
        UPDATE lineas_albaran_ruta SET
            cabecera_id = %s,
            fecha_albaran = %s,
            num_alb_ruta = %s,
            serie_alb = %s,
            numero_alb = %s,
            nombre_cliente = %s,
            cod_cliente = %s,
            municipio_envio = %s,
            importe = %s,
            beneficio = %s,
            imp_liqu = %s,
            porcentaje = %s,
            conductor = %s,
            tlpa = %s,
            ben_post_log = %s,
            por_ben_real = %s,
            deuda = %s,
            lineas = %s,
            fecha_registro = %s,
            fecha_alb = %s
        WHERE id = %s;
        """
        valores = (
            self.cabecera_id, self.fecha_albaran, self.num_alb_ruta,
            self.serie_alb, self.numero_alb, self.nombre_cliente,
            self.cod_cliente, self.municipio_envio, self.importe,
            self.beneficio, self.imp_liqu, self.porcentaje,
            self.conductor, self.tlpa, self.ben_post_log,
            self.por_ben_real, self.deuda, self.lineas,
            self.fecha_registro, self.fecha_alb, self.id
        )
        bd.ejecutar_sql(sql, valores)
        return True

    def eliminar(self):
        if self.id is None:
            return False
        bd = BDPostgresql()
        sql = "DELETE FROM lineas_albaran_ruta WHERE id = %s;"
        bd.ejecutar_sql(sql, (self.id,))
        return True

    def obtener_por_id(self, id):
        bd = BDPostgresql()
        sql = "SELECT * FROM lineas_albaran_ruta WHERE id = %s;"
        resultado = bd.ejecutar_sql(sql, (id,))
        if resultado:
            self.id = resultado[0]
            self.cabecera_id = resultado[1]
            self.fecha_albaran = resultado[2]
            self.num_alb_ruta = resultado[3]
            self.serie_alb = resultado[4]
            self.numero_alb = resultado[5]
            self.nombre_cliente = resultado[6]
            self.cod_cliente = resultado[7]
            self.municipio_envio = resultado[8]
            self.importe = resultado[9]
            self.beneficio = resultado[10]
            self.imp_liqu = resultado[11]
            self.porcentaje = resultado[12]
            self.conductor = resultado[13]
            self.tlpa = resultado[14]
            self.ben_post_log = resultado[15]
            self.por_ben_real = resultado[16]
            self.deuda = resultado[17]
            self.lineas = resultado[18]
            self.fecha_registro = resultado[19]
            self.fecha_alb = resultado[20]
            return True
        return False

    def obtener_por_cabecera(self, cabecera_id):
        bd = BDPostgresql()
        sql = "SELECT * FROM lineas_albaran_ruta WHERE cabecera_id = %s;"
        resultados = bd.ejecutar_sql(sql, (cabecera_id,))
        return resultados 