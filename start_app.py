#!/usr/bin/env python3
"""
Script mejorado para iniciar la aplicación Flask
"""

import sys
import os
from datetime import datetime

def main():
    """Función principal para iniciar la aplicación"""
    print("🚀 Iniciando Sistema de Gestión de Rutas - Mimoun Market SL")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Verificar que estamos en el entorno virtual
        if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("⚠️  Advertencia: No parece que estés en un entorno virtual")
            print("   Se recomienda usar: .venv\\Scripts\\activate")
        
        # Importar la aplicación
        from app import create_app
        
        # Crear la aplicación
        app = create_app()
        
        print("✅ Aplicación Flask creada exitosamente")
        print(f"🌐 Servidor iniciando en: http://localhost:5000")
        print("📋 Rutas disponibles:")
        
        # Mostrar las rutas principales
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append((rule.rule, rule.endpoint))
        
        # Ordenar y mostrar rutas
        routes.sort(key=lambda x: x[0])
        for route, endpoint in routes:
            print(f"   {route} -> {endpoint}")
        
        print("\n" + "=" * 60)
        print("🎯 Para detener el servidor, presiona Ctrl+C")
        print("=" * 60)
        
        # Iniciar la aplicación
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrate de que todas las dependencias estén instaladas:")
        print("   .venv\\Scripts\\python.exe -m pip install -r requirements.txt")
        return 1
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 