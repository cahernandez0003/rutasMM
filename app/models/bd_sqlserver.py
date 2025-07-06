import pyodbc
from app.config import Config

class BDSqlServer:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.conectar()

    def conectar(self):
        try:
            self.conn = pyodbc.connect(
                'DRIVER={SQL Server};'
                f'SERVER={Config.SQLSERVER_HOST};'
                f'DATABASE={Config.SQLSERVER_DB};'
                f'UID={Config.SQLSERVER_USER};'
                f'PWD={Config.SQLSERVER_PASSWORD}'
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Error al conectar a SQL Server: {str(e)}")
            raise

    def ejecutar_sql(self, sql, params=None):
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al ejecutar SQL: {str(e)}")
            raise
        
    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close() 