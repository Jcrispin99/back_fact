# Documentación de Endpoints - Companies API

## Base URL
```
http://localhost:8000/api/v1/
```

## Autenticación
Todos los endpoints requieren autenticación. Incluir en headers:
```
Authorization: Bearer <token>
```

---

## 📋 COMPANIES ENDPOINTS

### 1. Listar Empresas
**GET** `/companies/`

**Descripción:** Obtiene la lista de empresas según el rol del usuario
- Super Admin: Ve todas las empresas activas
- Admin: Ve su empresa y sus sucursales

**Query Parameters (opcionales):**
- `tipo_empresa`: Filtrar por tipo (farmacia, ropa, abarrotes, restaurante, otros)
- `plan_suscripcion`: Filtrar por plan
- `parent`: Filtrar por empresa padre (ID)
- `search`: Buscar por nombre o RUC
- `ordering`: Ordenar por nombre o fecha_registro (ej: `-nombre`, `fecha_registro`)

**Respuesta exitosa (200):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "nombre": "TechCorp Solutions SAC",
      "ruc": "20123456789",
      "tipo_empresa": "otros",
      "direccion": "Av. Javier Prado 123, San Isidro",
      "telefono": "01-2345678",
      "email": "contacto@techcorp.com.pe",
      "logo_url": "https://techcorp.com.pe/logo.png",
      "plan_suscripcion": "premium",
      "estado": true,
      "parent": null,
      "sucursales": [2],
      "ubicaciones": [
        {
          "id": 1,
          "empresa": 1,
          "nombre": "Almacén Principal",
          "direccion": "Av. Javier Prado 123, San Isidro",
          "es_almacen_principal": true,
          "estado": true
        }
      ]
    }
  ]
}
```

### 2. Crear Empresa
**POST** `/companies/`

**Descripción:** Crea una nueva empresa (solo Super Admin)

**Campos requeridos:**
```json
{
  "nombre": "string (max 255 chars)",
  "ruc": "string (11 chars, único)",
  "tipo_empresa": "string (farmacia|ropa|abarrotes|restaurante|otros)"
}
```

**Campos opcionales:**
```json
{
  "parent": "integer (ID de empresa padre para sucursales)",
  "direccion": "string (max 255 chars)",
  "telefono": "string (max 20 chars)",
  "email": "string (email válido)",
  "logo_url": "string (URL válida)",
  "plan_suscripcion": "string (default: 'free')",
  "estado": "boolean (default: true)"
}
```

**Ejemplo de request:**
```json
{
  "nombre": "Mi Empresa SAC",
  "ruc": "20987654321",
  "tipo_empresa": "farmacia",
  "direccion": "Av. Principal 456",
  "telefono": "01-9876543",
  "email": "contacto@miempresa.com",
  "plan_suscripcion": "basic"
}
```

### 3. Obtener Empresa por ID
**GET** `/companies/{id}/`

**Descripción:** Obtiene los detalles de una empresa específica

**Permisos:**
- Super Admin: Cualquier empresa
- Admin: Solo su empresa o sucursales

### 4. Actualizar Empresa
**PUT** `/companies/{id}/` o **PATCH** `/companies/{id}/`

**Descripción:** Actualiza una empresa existente

**Permisos:**
- Super Admin: Cualquier empresa
- Admin: Solo su empresa

**Campos actualizables:** Los mismos que en crear empresa

### 5. Eliminar Empresa
**DELETE** `/companies/{id}/`

**Descripción:** Elimina (desactiva) una empresa

**Permisos:**
- Super Admin: Cualquier empresa
- Admin: Solo su empresa

---

## 📍 LOCATIONS ENDPOINTS

### 1. Listar Ubicaciones
**GET** `/locations/`

**Descripción:** Obtiene la lista de ubicaciones según el rol del usuario
- Super Admin: Ve todas las ubicaciones activas
- Admin: Ve ubicaciones de su empresa y sucursales

**Query Parameters (opcionales):**
- `empresa`: Filtrar por empresa (ID)
- `es_almacen_principal`: Filtrar por almacén principal (true/false)
- `search`: Buscar por nombre o dirección

**Respuesta exitosa (200):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "empresa": 1,
      "nombre": "Almacén Principal",
      "direccion": "Av. Javier Prado 123, San Isidro",
      "es_almacen_principal": true,
      "estado": true
    }
  ]
}
```

### 2. Crear Ubicación
**POST** `/locations/`

**Descripción:** Crea una nueva ubicación para una empresa

**Campos requeridos:**
```json
{
  "empresa": "integer (ID de la empresa)",
  "nombre": "string (max 100 chars)"
}
```

**Campos opcionales:**
```json
{
  "direccion": "string (max 255 chars)",
  "es_almacen_principal": "boolean (default: false)",
  "estado": "boolean (default: true)"
}
```

**Ejemplo de request:**
```json
{
  "empresa": 1,
  "nombre": "Sucursal Norte",
  "direccion": "Av. Los Olivos 789, Los Olivos",
  "es_almacen_principal": false
}
```

### 3. Obtener Ubicación por ID
**GET** `/locations/{id}/`

**Descripción:** Obtiene los detalles de una ubicación específica

### 4. Actualizar Ubicación
**PUT** `/locations/{id}/` o **PATCH** `/locations/{id}/`

**Descripción:** Actualiza una ubicación existente

**Campos actualizables:** Los mismos que en crear ubicación

### 5. Eliminar Ubicación
**DELETE** `/locations/{id}/`

**Descripción:** Elimina (desactiva) una ubicación

---

## 🔒 Permisos y Restricciones

### Super Admin
- Acceso completo a todas las empresas y ubicaciones
- Puede crear, leer, actualizar y eliminar cualquier registro

### Admin de Empresa
- Solo puede ver y gestionar su empresa y sus sucursales
- Solo puede ver ubicaciones de su empresa y sucursales
- No puede eliminar su propia empresa

### Empleado
- Sin acceso a estos endpoints (solo lectura limitada según otros permisos)

---

## 📝 Notas Importantes

1. **RUC único:** El RUC debe ser único en todo el sistema
2. **Sucursales:** Para crear una sucursal, incluir el campo `parent` con el ID de la empresa principal
3. **Ubicaciones únicas:** El nombre de ubicación debe ser único por empresa
4. **Estados:** Los registros eliminados se marcan como `estado: false` (soft delete)
5. **Filtros:** Todos los endpoints de listado soportan filtros y búsqueda
6. **Paginación:** Los resultados están paginados por defecto

---

## 🧪 Datos de Prueba Disponibles

Puedes usar los datos creados en `DATOS_EJEMPLO.md` para probar estos endpoints.

**Empresas de ejemplo:**
- TechCorp Solutions SAC (RUC: 20123456789)
- Comercial Andina EIRL (RUC: 20234567890)
- Servicios Integrales del Sur SA (RUC: 20345678901)
- TechCorp - Sucursal Miraflores (sucursal de TechCorp)

**Credenciales de prueba:**
- Super Admin: `superadmin_sunat` / `admin123`
- Admin TechCorp: `carlos_techcorp` / `admin123`
- Admin Andina: `maria_andina` / `admin123`