# Sistema de rutas logísticas

Este proyecto es una base modular para el desarrollo de un sistema Flask destinado al control y gestión de rutas logísticas, incluyendo albaranes, transportistas, usuarios y más. 096f633612f24d13dd066cf91e13428460770bfa

## Estructura principal

- **app/**: Módulo principal de la aplicación Flask.
  - **routes/**: Blueprints para cada módulo (rutas, usuarios, transportistas, albaranes, etc.)
  - **models/**: Conexiones y lógica de base de datos.
  - **templates/**: Vistas y fragmentos HTML.
    - **includes/**: Navbar, header, footer, etc.
    - **pages/**: Páginas específicas de cada módulo.
- **static/**: Archivos estáticos (CSS, JS, imágenes).
- **run.py**: Punto de entrada de la aplicación.
- **README.md**: Este archivo.
- **diario.txt**: Bitácora de cambios y decisiones.
- **LICENSE**: Licencia del proyecto (si aplica).

## Requisitos

- Python 3.12+
- Flask 3.1+
- PostgreSQL 15+
- SQL Server (solo lectura)
- Bootstrap 5.3 (CDN)

## Uso rápido


# Activa tu entorno virtual
- python -m venv .venv
- .venv\Scripts\activate  # en Windows

# Instala dependencias
- pip install flask

# Ejecuta la app
- python run.py
