# Sistema de Gestión de Rutas - Mimoun Market SL

Sistema web para la gestión de rutas de transporte, transportistas, usuarios y albaranes.

## 🚀 Características

- **Gestión de Rutas**: Crear, editar y eliminar rutas de transporte
- **Gestión de Transportistas**: Administrar información de transportistas
- **Gestión de Usuarios**: Sistema de usuarios con roles y autenticación
- **Albaranes**: Creación y gestión de albaranes de ruta
- **Base de Datos**: Soporte para PostgreSQL y SQL Server
- **Interfaz Web**: Interfaz moderna con Bootstrap y DataTables

## 📋 Requisitos

- Python 3.8 o superior
- PostgreSQL (base de datos principal)
- SQL Server (opcional, para integración con ERP)
- Navegador web moderno

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd rutas
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar base de datos

#### PostgreSQL (Requerido)
1. Crear base de datos `logistica_rutas`
2. Ejecutar el script SQL: `rutas.sql`
3. Configurar conexión en `app/models/bd_postgresql.py`

#### SQL Server (Opcional)
1. Configurar conexión en `app/models/bd.py`
2. Asegurar que el driver ODBC esté instalado

## 🚀 Uso

### Iniciar la aplicación

**Opción 1: Script mejorado (Recomendado)**
```bash
python start_app.py
```

**Opción 2: Script básico**
```bash
python run.py
```

### Acceder a la aplicación
- URL: http://localhost:5000
- Usuario por defecto: Crear en la base de datos

## 📁 Estructura del Proyecto

```
rutas/
├── app/
│   ├── models/          # Modelos de datos
│   ├── routes/          # Rutas de la aplicación
│   ├── templates/       # Plantillas HTML
│   ├── config.py        # Configuración
│   └── decorators.py    # Decoradores de autenticación
├── static/              # Archivos estáticos
├── requirements.txt     # Dependencias Python
├── run.py              # Script de inicio básico
├── start_app.py        # Script de inicio mejorado
└── test_app.py         # Script de pruebas
```

## 🔧 Configuración

### Variables de entorno
- `SECRET_KEY`: Clave secreta para sesiones (opcional)

### Base de datos
- Configurar conexiones en `app/models/bd_postgresql.py` y `app/models/bd.py`
- Asegurar que las tablas estén creadas según `rutas.sql`

## 🧪 Pruebas

Ejecutar el script de pruebas:
```bash
python test_app.py
```

## 📝 Funcionalidades

### Autenticación
- Login/logout de usuarios
- Control de acceso por roles
- Registro de intentos de login

### Gestión de Rutas
- CRUD completo de rutas
- Códigos y nombres de ruta
- Estado activo/inactivo

### Gestión de Transportistas
- Información completa de transportistas
- Datos de contacto y documentación
- Estado activo/inactivo

### Gestión de Usuarios
- Creación y edición de usuarios
- Roles: admin, supus
- Contraseñas hasheadas

### Albaranes
- Creación de cabeceras de albarán
- Integración con rutas y transportistas
- Cálculo automático de porcentajes

## 🐛 Solución de Problemas

### Error de conexión a PostgreSQL
- Verificar que PostgreSQL esté ejecutándose
- Comprobar credenciales en `bd_postgresql.py`
- Asegurar que la base de datos existe

### Error de módulos no encontrados
- Activar el entorno virtual
- Instalar dependencias: `pip install -r requirements.txt`

### Error de políticas de PowerShell
- Ejecutar: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- O usar directamente: `.venv\Scripts\python.exe start_app.py`

## 📞 Soporte

Para soporte técnico, contactar al equipo de desarrollo.

## 📄 Licencia

Este proyecto está bajo la licencia especificada en el archivo LICENSE.
