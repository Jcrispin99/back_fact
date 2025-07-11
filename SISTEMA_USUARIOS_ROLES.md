# 📋 Sistema de Usuarios y Roles - Documentación Actualizada

## 🔄 Cambios Implementados en el Sistema

### ❌ Sistema Anterior (Django Groups)
- Usaba `django.contrib.auth.models.Group`
- Relaciones many-to-many complejas
- Permisos granulares por grupo
- Consultas con JOINs adicionales

### ✅ Sistema Actual (Roles Personalizados)
- Campo `rol` directo en el modelo User
- 3 roles específicos: `empleado`, `admin`, `super_admin`
- Propiedades calculadas: `is_admin`, `is_super_admin`
- Mejor performance y simplicidad

---

## 🏗️ Arquitectura del Sistema

### 📊 Modelo User Actualizado

```python
class User(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('super_admin', 'Super Administrador'),
    ]
    
    email = models.EmailField(unique=True)  # LOGIN FIELD
    empresa = models.ForeignKey('companies.Company', ...)
    rol = models.CharField(max_length=20, choices=ROLES, default='empleado')
    estado = models.BooleanField(default=True)
    telefono = models.CharField(max_length=20, blank=True)
    
    @property
    def is_admin(self):
        return self.rol == 'admin' or self.rol == 'super_admin'
    
    @property
    def is_super_admin(self):
        return self.rol == 'super_admin'
```

### 🔐 Jerarquía de Permisos

| Rol | Nivel | Permisos |
|-----|-------|----------|
| **super_admin** | 🔴 Máximo | - Ve TODAS las empresas<br>- Crea/edita cualquier usuario<br>- Cambia roles<br>- Acceso total |
| **admin** | 🟡 Medio | - Ve SU empresa + sucursales<br>- Crea usuarios de su empresa<br>- NO puede cambiar roles<br>- Gestiona su empresa |
| **empleado** | 🟢 Básico | - Ve solo su perfil<br>- NO gestiona usuarios<br>- NO ve empresas<br>- Acceso limitado |

---

## 🌐 API Endpoints Actualizados

### 🔑 Autenticación (Djoser)

```bash
# Registro público
POST /api/v1/auth/users/
{
    "email": "usuario@empresa.com",
    "username": "usuario123",
    "first_name": "Juan",
    "last_name": "Pérez",
    "password": "contraseña123",
    "re_password": "contraseña123",
    "telefono": "+51987654321",
    "empresa": 1,
    "rol": "empleado"  # Solo empleado por defecto
}

# Login
POST /api/v1/auth/jwt/create/
{
    "email": "usuario@empresa.com",
    "password": "contraseña123"
}

# Refresh Token
POST /api/v1/auth/jwt/refresh/
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 👥 Gestión de Usuarios

```bash
# Listar usuarios (filtrado por permisos)
GET /api/v1/users/
# Super admin: ve todos
# Admin: ve solo de su empresa
# Empleado: ve solo su perfil

# Crear usuario (requiere autenticación)
POST /api/v1/users/
{
    "email": "nuevo@empresa.com",
    "username": "nuevo123",
    "first_name": "Nuevo",
    "last_name": "Usuario",
    "password": "contraseña123",
    "telefono": "+51987654321",
    "empresa": 1,
    "rol": "empleado"  # Solo super_admin puede asignar admin/super_admin
}

# Actualizar usuario
PATCH /api/v1/users/{id}/
{
    "first_name": "Nombre Actualizado",
    "last_name": "Apellido Actualizado",
    "telefono": "+51999888777",
    "empresa": 2,  # Solo super_admin puede cambiar empresa
    "rol": "admin",  # Solo super_admin puede cambiar roles
    "estado": true
}

# Cambiar contraseña
POST /api/v1/users/{id}/change_password/
{
    "old_password": "contraseña_actual",
    "new_password": "nueva_contraseña",
    "confirm_password": "nueva_contraseña"
}

# Perfil actual
GET /api/v1/users/me/

# Estadísticas (solo admins)
GET /api/v1/users/stats/
```

---

## 🎨 Cambios Requeridos en el Frontend

### 🔄 Respuesta de Usuario Actualizada

```typescript
interface User {
    id: number;
    email: string;
    username: string;
    first_name: string;
    last_name: string;
    telefono: string;
    empresa: number | null;
    empresa_nombre: string;  // Nuevo campo
    rol: 'empleado' | 'admin' | 'super_admin';  // Actualizado
    rol_display: string;  // Nuevo campo
    estado: boolean;
    is_admin: boolean;  // Nuevo campo calculado
    is_super_admin: boolean;  // Nuevo campo calculado
    date_joined: string;
    fecha_creacion: string;
    fecha_actualizacion: string;
}
```

### 🛡️ Guards de Rutas Actualizados

```typescript
// Reemplazar verificaciones de grupos por roles

// ANTES (con grupos)
if (user.groups.includes('Administradores')) {
    // lógica admin
}

// AHORA (con roles)
if (user.is_admin) {
    // lógica admin
}

if (user.is_super_admin) {
    // lógica super admin
}

if (user.rol === 'empleado') {
    // lógica empleado
}
```

### 🎯 Componentes de UI Actualizados

```tsx
// Selector de roles
const RoleSelector = ({ user, currentUser }) => {
    const canChangeRole = currentUser.is_super_admin;
    
    return (
        <select 
            value={user.rol} 
            disabled={!canChangeRole}
            onChange={handleRoleChange}
        >
            <option value="empleado">Empleado</option>
            <option value="admin">Administrador</option>
            {currentUser.is_super_admin && (
                <option value="super_admin">Super Administrador</option>
            )}
        </select>
    );
};

// Badge de rol
const RoleBadge = ({ user }) => {
    const roleColors = {
        'empleado': 'bg-green-100 text-green-800',
        'admin': 'bg-yellow-100 text-yellow-800',
        'super_admin': 'bg-red-100 text-red-800'
    };
    
    return (
        <span className={`px-2 py-1 rounded-full text-xs ${roleColors[user.rol]}`}>
            {user.rol_display}
        </span>
    );
};
```

### 📱 Navegación Condicional

```tsx
const Navigation = ({ user }) => {
    return (
        <nav>
            {/* Todos los usuarios */}
            <Link to="/profile">Mi Perfil</Link>
            
            {/* Solo admins y super admins */}
            {user.is_admin && (
                <>
                    <Link to="/users">Gestión de Usuarios</Link>
                    <Link to="/companies">Mi Empresa</Link>
                </>
            )}
            
            {/* Solo super admins */}
            {user.is_super_admin && (
                <>
                    <Link to="/all-companies">Todas las Empresas</Link>
                    <Link to="/system-settings">Configuración del Sistema</Link>
                </>
            )}
        </nav>
    );
};
```

---

## 🚨 Errores Comunes y Soluciones

### ❌ Error: "No tienes permisos para cambiar el rol"
**Causa:** Usuario no es super_admin
**Solución:** Solo super_admin puede cambiar roles

### ❌ Error: Campos de solo lectura en actualización
**Causa:** UserUpdateSerializer limita campos editables
**Solución:** Usar endpoints específicos para email, username, contraseña

### ❌ Error: Usuario no ve empresas
**Causa:** Empleados no tienen acceso a gestión de empresas
**Solución:** Cambiar rol a admin o super_admin

---

## 🔧 Configuración de Desarrollo

### Crear Super Admin Inicial

```bash
# Opción 1: Django Shell
python manage.py shell

from users.models import User
super_admin = User.objects.create_user(
    email='superadmin@test.com',
    username='superadmin',
    first_name='Super',
    last_name='Admin',
    password='admin123',
    rol='super_admin'
)

# Opción 2: Django Admin
python manage.py createsuperuser
# Luego cambiar rol en admin panel
```

### Variables de Entorno

```env
# JWT Configuration
ACCESS_TOKEN_LIFETIME=60  # minutos
REFRESH_TOKEN_LIFETIME=7  # días

# Djoser Configuration
SEND_ACTIVATION_EMAIL=True
USER_CREATE_PASSWORD_RETYPE=True
```

---

## 📝 Checklist de Migración Frontend

- [ ] Actualizar interfaces TypeScript
- [ ] Reemplazar verificaciones de grupos por roles
- [ ] Actualizar guards de rutas
- [ ] Modificar componentes de gestión de usuarios
- [ ] Implementar navegación condicional
- [ ] Actualizar formularios de registro/edición
- [ ] Probar flujos de permisos
- [ ] Documentar cambios para el equipo

---

**📅 Fecha de actualización:** $(date)
**🔄 Versión del sistema:** v2.0 - Roles Personalizados
**👨‍💻 Responsable:** Equipo de Desarrollo

> **Nota para IA:** Este sistema reemplaza completamente el manejo de grupos de Django por un sistema de roles más simple y eficiente. Todos los permisos ahora se basan en el campo `rol` del usuario y las propiedades calculadas `is_admin` e `is_super_admin`.