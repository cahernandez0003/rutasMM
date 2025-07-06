import pyodbc

class BD:
    """Clase base para todos los modelos que interactúan con la base de datos."""
    def __init__(self):
        pass

    def to_dict(self):
        """Convierte el objeto a un diccionario."""
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}

    @staticmethod
    def from_dict(data):
        """Crea una instancia desde un diccionario."""
        instance = BD()
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

def get_sqlserver_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=10.0.05\\SAGE200;"        # Usar doble backslash para la secuencia de escape
            "DATABASE=MMARKET;"               # Tu base de datos ERP
            "UID=consultasMM;"                # Usuario SQL Server
            "PWD=Sage2009+;"                  # Contraseña SQL Server
            "TrustServerCertificate=yes;"     # Opción útil para entornos locales
        )
        return conn
    except Exception as e:
        print(f"Error conectando a SQL Server: {e}")
        return None
