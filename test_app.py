#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación Flask funciona correctamente
"""

import sys
import traceback

def test_imports():
    """Prueba las importaciones principales"""
    print("🔍 Probando importaciones...")
    
    try:
        from app import create_app
        print("✅ Importación de create_app exitosa")
    except Exception as e:
        print(f"❌ Error en importación de create_app: {e}")
        return False
    
    try:
        from app.models.bd_postgresql import get_postgresql_connection
        print("✅ Importación de conexión PostgreSQL exitosa")
    except Exception as e:
        print(f"❌ Error en importación de PostgreSQL: {e}")
        return False
    
    try:
        from app.models.bd import get_sqlserver_connection
        print("✅ Importación de conexión SQL Server exitosa")
    except Exception as e:
        print(f"❌ Error en importación de SQL Server: {e}")
        return False
    
    return True

def test_database_connections():
    """Prueba las conexiones a bases de datos"""
    print("\n🔍 Probando conexiones a bases de datos...")
    
    # Prueba PostgreSQL
    try:
        from app.models.bd_postgresql import get_postgresql_connection
        conn = get_postgresql_connection()
        if conn:
            print("✅ Conexión a PostgreSQL exitosa")
            conn.close()
        else:
            print("❌ No se pudo conectar a PostgreSQL")
            return False
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return False
    
    # Prueba SQL Server
    try:
        from app.models.bd import get_sqlserver_connection
        conn = get_sqlserver_connection()
        if conn:
            print("✅ Conexión a SQL Server exitosa")
            conn.close()
        else:
            print("⚠️  No se pudo conectar a SQL Server (puede ser normal si no está configurado)")
    except Exception as e:
        print(f"⚠️  Error conectando a SQL Server: {e} (puede ser normal si no está configurado)")
    
    return True

def test_flask_app():
    """Prueba la creación de la aplicación Flask"""
    print("\n🔍 Probando creación de aplicación Flask...")
    
    try:
        from app import create_app
        app = create_app()
        print("✅ Aplicación Flask creada exitosamente")
        
        # Verificar que las rutas están registradas
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        print(f"✅ Rutas registradas: {len(routes)} rutas encontradas")
        
        return True
    except Exception as e:
        print(f"❌ Error creando aplicación Flask: {e}")
        traceback.print_exc()
        return False

def test_models():
    """Prueba los modelos principales"""
    print("\n🔍 Probando modelos...")
    
    try:
        from app.models.usuarios import get_all_usuarios
        print("✅ Modelo de usuarios importado correctamente")
    except Exception as e:
        print(f"❌ Error en modelo de usuarios: {e}")
        return False
    
    try:
        from app.models.rutas import get_all_rutas
        print("✅ Modelo de rutas importado correctamente")
    except Exception as e:
        print(f"❌ Error en modelo de rutas: {e}")
        return False
    
    try:
        from app.models.transportistas import get_all_transportistas
        print("✅ Modelo de transportistas importado correctamente")
    except Exception as e:
        print(f"❌ Error en modelo de transportistas: {e}")
        return False
    
    return True

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas del sistema de rutas...\n")
    
    tests = [
        ("Importaciones", test_imports),
        ("Conexiones BD", test_database_connections),
        ("Aplicación Flask", test_flask_app),
        ("Modelos", test_models)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"📋 Ejecutando prueba: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASÓ\n")
        else:
            print(f"❌ {test_name}: FALLÓ\n")
    
    print(f"📊 Resumen: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está listo para usar.")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 