from app.models.bd import get_sqlserver_connection

conn = get_sqlserver_connection()
if conn:
    print("Conexión exitosa a SQL Server!")
    conn.close()
else:
    print("No se pudo conectar.")
