import pyodbc

def get_sqlserver_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=10.0.05\SAGE200;"         # Ejemplo: localhost\SQLEXPRESS o IP, o nombre de red
            "DATABASE=MMARKET;"     # Tu base de datos ERP
            "UID=consultasMM;"                # Usuario SQL Server
            "PWD=Sage2009+;"             # Contraseña SQL Server
            "TrustServerCertificate=yes;"     # Opción útil para entornos locales
        )
        return conn
    except Exception as e:
        print(f"Error conectando a SQL Server: {e}")
        return None
