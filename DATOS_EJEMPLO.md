# 📊 Datos de Ejemplo - Sistema SUNAT

## 🎯 Resumen

Se han creado datos de ejemplo para facilitar las pruebas e interacción con el sistema. Los datos incluyen empresas, usuarios con diferentes roles y ubicaciones.

## 📈 Datos Creados

### 🏢 Empresas (4 total)
- **TechCorp Solutions SAC** (RUC: 20123456789) - Principal
- **Comercial Andina EIRL** (RUC: 20987654321) - Principal  
- **Servicios Integrales del Sur SA** (RUC: 20456789123) - Principal
- **TechCorp - Sucursal Miraflores** (RUC: 20123456790) - Sucursal de TechCorp

### 👥 Usuarios (7 total)

#### 👑 Super Administradores (3)
- `superadmin@sunat.com` - Nuevo super admin creado
- `superadmin@test.com` - Existía previamente
- `admin@test.com` - Existía previamente

#### 👨‍💼 Administradores de Empresa (2)
- `admin@techcorp.com.pe` - Carlos Mendoza (TechCorp Solutions SAC)
- `admin@comercialandina.pe` - María García (Comercial Andina EIRL)

#### 👥 Empleados (2)
- `juan.perez@techcorp.com.pe` - Juan Pérez (TechCorp Solutions SAC)
- `pedro.silva@comercialandina.pe` - Pedro Silva (Comercial Andina EIRL)

### 📍 Ubicaciones (2 total)
- **Almacén Principal TechCorp** - TechCorp Solutions SAC (Almacén Principal)
- **Tienda Principal Andina** - Comercial Andina EIRL (Ubicación)

## 🔑 Credenciales de Acceso

### Para Pruebas de API

```bash
# Super Administrador
Email: superadmin@sunat.com
Password: admin123

# Administrador TechCorp
Email: admin@techcorp.com.pe
Password: admin123

# Administrador Andina
Email: admin@comercialandina.pe
Password: admin123

# Empleado TechCorp
Email: juan.perez@techcorp.com.pe
Password: empleado123

# Empleado Andina
Email: pedro.silva@comercialandina.pe
Password: empleado123
```

## 🚀 Cómo Usar los Datos

### 1. Autenticación
```bash
# Obtener token JWT
curl -X POST http://localhost:8000/api/v1/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "superadmin@sunat.com",
    "password": "admin123"
  }'
```

### 2. Consultar Empresas
```bash
# Como Super Admin (ve todas las empresas)
curl -X GET http://localhost:8000/api/v1/companies/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Como Admin de empresa (ve su empresa y sucursales)
curl -X GET http://localhost:8000/api/v1/companies/ \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### 3. Consultar Usuarios
```bash
# Como Super Admin (ve todos los usuarios)
curl -X GET http://localhost:8000/api/v1/users/ \
  -H "Authorization: Bearer SUPERADMIN_TOKEN"

# Como Admin (ve usuarios de su empresa)
curl -X GET http://localhost:8000/api/v1/users/ \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### 4. Consultar Ubicaciones
```bash
# Obtener ubicaciones
curl -X GET http://localhost:8000/api/v1/locations/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔄 Regenerar Datos

Si necesitas regenerar los datos de ejemplo:

```bash
# Ejecutar el script de creación
python create_sample_data.py

# Verificar los datos creados
python check_data.py
```

## 🧪 Casos de Prueba Sugeridos

### Pruebas de Permisos
1. **Super Admin**: Puede ver y gestionar todas las empresas y usuarios
2. **Admin de Empresa**: Solo puede ver su empresa, sucursales y usuarios asociados
3. **Empleado**: Solo puede ver su propia información

### Pruebas de Funcionalidad
1. **Gestión de Empresas**: Crear, editar, eliminar empresas y sucursales
2. **Gestión de Usuarios**: Crear usuarios, asignar roles, cambiar empresas
3. **Gestión de Ubicaciones**: Crear y gestionar ubicaciones por empresa

### Pruebas de Jerarquía
1. **Relación Empresa-Sucursal**: TechCorp tiene una sucursal en Miraflores
2. **Usuarios por Empresa**: Cada empresa tiene su admin y empleados
3. **Ubicaciones por Empresa**: Cada empresa tiene sus ubicaciones específicas

## 📝 Notas Importantes

- Los datos se crean usando `get_or_create()`, por lo que ejecutar el script múltiples veces no duplicará los datos
- Las contraseñas están hasheadas usando el sistema de Django
- Los super admins no tienen empresa asignada (pueden gestionar todas)
- Los admins y empleados están asignados a empresas específicas

## 🛠️ Archivos Relacionados

- `create_sample_data.py` - Script para crear los datos de ejemplo
- `check_data.py` - Script para verificar los datos creados
- `SISTEMA_USUARIOS_ROLES.md` - Documentación completa del sistema de roles

¡Ahora puedes probar e interactuar con el sistema usando estos datos de ejemplo! 🎉