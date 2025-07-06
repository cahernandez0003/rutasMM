import os

class Config:
    # Configuración PostgreSQL
    POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST', 'localhost')
    POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT', '5432')
    POSTGRESQL_DB = os.getenv('POSTGRESQL_DB', 'rutas')
    POSTGRESQL_USER = os.getenv('POSTGRESQL_USER', 'postgres')
    POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD', 'postgres')

    # Configuración SQL Server
    SQLSERVER_HOST = os.getenv('SQLSERVER_HOST', 'localhost')
    SQLSERVER_DB = os.getenv('SQLSERVER_DB', 'MMARKET')
    SQLSERVER_USER = os.getenv('SQLSERVER_USER', 'sa')
    SQLSERVER_PASSWORD = os.getenv('SQLSERVER_PASSWORD', 'password')

    # Configuración de la aplicación
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    DEBUG = os.getenv('FLASK_DEBUG', True)
