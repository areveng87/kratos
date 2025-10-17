# Kratos - Sistema de Gestión de Muebles

Sistema completo de gestión para empresas de muebles con frontend en Vue.js y backend en Python FastAPI.

## Características

- 🔐 **Autenticación JWT** - Sistema seguro de login con roles de usuario
- 📊 **Dashboard Interactivo** - Métricas en tiempo real y gráficos
- 🏢 **Gestión de Empresas** - CRUD completo de empresas y clientes
- 💼 **Operaciones Comerciales** - Seguimiento de compras, ventas y transferencias
- 🎨 **Diseño Moderno** - Interfaz oscura y profesional
- 📱 **Responsive** - Adaptado para desktop y móvil

## Tecnologías

### Frontend
- Vue.js 3 con Composition API
- Vue Router para navegación
- Pinia para manejo de estado
- Tailwind CSS para estilos
- Lucide Vue para iconos
- Axios para peticiones HTTP

### Backend
- FastAPI (Python)
- SQL Server como base de datos
- JWT para autenticación
- Bcrypt para hash de contraseñas
- Pydantic para validación de datos

## Instalación

### Prerrequisitos
- Node.js 18+
- Python 3.8+
- SQL Server

### Backend

1. Navegar al directorio backend:
\`\`\`bash
cd backend
\`\`\`

2. Crear entorno virtual:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
\`\`\`

3. Instalar dependencias:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Configurar variables de entorno:
\`\`\`bash
cp .env.example .env
# Editar .env con tus credenciales de SQL Server
\`\`\`

5. Ejecutar scripts de base de datos:
\`\`\`bash
# Ejecutar scripts en SQL Server Management Studio o similar
# 01_create_database.sql
# 02_insert_initial_data.sql
\`\`\`

6. Iniciar servidor:
\`\`\`bash
python main.py
\`\`\`

### Frontend

1. Navegar al directorio frontend:
\`\`\`bash
cd frontend
\`\`\`

2. Instalar dependencias:
\`\`\`bash
npm install
\`\`\`

3. Iniciar servidor de desarrollo:
\`\`\`bash
npm run dev
\`\`\`

## Uso

1. Acceder a http://localhost:3000
2. Usar credenciales de prueba:
   - Email: admin@kratos.com
   - Password: admin123

## Estructura del Proyecto

\`\`\`
kratos/
├── backend/
│   ├── main.py              # Aplicación FastAPI principal
│   ├── models.py            # Modelos Pydantic
│   ├── services.py          # Lógica de negocio
│   ├── auth.py              # Autenticación JWT
│   ├── database.py          # Conexión a base de datos
│   └── requirements.txt     # Dependencias Python
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes Vue reutilizables
│   │   ├── views/           # Páginas principales
│   │   ├── stores/          # Estado global (Pinia)
│   │   ├── router/          # Configuración de rutas
│   │   └── api/             # Cliente HTTP
│   └── package.json         # Dependencias Node.js
└── scripts/
    ├── 01_create_database.sql
    └── 02_insert_initial_data.sql
\`\`\`

## Roles de Usuario

- **Administrador**: Acceso completo al sistema
- **Analista PBC**: Análisis de operaciones PBC
- **OCI Interno/Externo**: Operaciones internas y externas
- **SPV**: Gestión de vehículos especiales
- **Servicer Supervisor/Operador**: Supervisión y operación de servicios
- **Auditor**: Auditoría y revisión

## API Endpoints

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener usuario actual

### Dashboard
- `GET /api/dashboard/stats` - Estadísticas del dashboard
- `GET /api/dashboard/chart-data` - Datos para gráficos

### Operaciones
- `GET /api/operaciones` - Listar operaciones
- `POST /api/operaciones` - Crear operación

### Empresas
- `GET /api/empresas` - Listar empresas
- `POST /api/empresas` - Crear empresa

## Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.
