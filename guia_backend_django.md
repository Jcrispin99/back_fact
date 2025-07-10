# Guía del Backend Django - Sistema de Facturación SUNAT

## Descripción General

Este proyecto Django implementa un sistema de facturación electrónica integrado con SUNAT para diferentes tipos de empresas (farmacias, tiendas de ropa, abarrotes, restaurantes, etc.).

## Estructura de Modelos

### 1. Empresa (Company)

Modelo principal que representa las empresas que utilizan el sistema.

```python
class Company(models.Model):
    TIPO_EMPRESA_CHOICES = [
        ('farmacia', 'Farmacia'),
        ('ropa', 'Tienda de Ropa'),
        ('abarrotes', 'Tienda de Abarrotes'),
        ('restaurante', 'Restaurante'),
        ('otros', 'Otros'),
    ]
    
    nombre = models.CharField(max_length=255)
    ruc = models.CharField(max_length=11, unique=True)
    tipo_empresa = models.CharField(max_length=20, choices=TIPO_EMPRESA_CHOICES)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    logo_url = models.URLField(blank=True)
    plan_suscripcion = models.CharField(max_length=20, default="free")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
```

**Características:**
- RUC único por empresa
- Soporte para múltiples tipos de negocio
- Sistema de suscripciones (free, premium, etc.)
- Estado activo/inactivo

### 2. Usuario (User)

Usuario personalizado que extiende AbstractUser con roles y asociación a empresa.

```python
class User(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
    ]
    empresa = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='empleado')
    estado = models.BooleanField(default=True)
```

**Características:**
- Sistema de roles (admin/empleado)
- Asociación a empresa específica
- Hereda funcionalidades de Django User

### 3. Producto (Product)

Catálogo de productos por empresa.

```python
class Product(models.Model):
    empresa = models.ForeignKey(Company, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField(default=0)
    unidad_medida = models.CharField(max_length=20, default="unidad")
    codigo_sunat = models.CharField(max_length=20, blank=True)
    imagen_url = models.URLField(blank=True)
```

**Características:**
- Productos específicos por empresa
- Control de precios de compra y venta
- Gestión de stock
- Códigos SUNAT para facturación electrónica

### 4. Ventas (Sale & SaleItem)

Sistema de ventas con soporte para boletas y facturas.

```python
class Sale(models.Model):
    TIPO_DOCUMENTO = [
        ('boleta', 'Boleta'),
        ('factura', 'Factura'),
    ]
    ESTADO = [
        ('emitida', 'Emitida'),
        ('anulada', 'Anulada'),
        ('enviada', 'Enviada a SUNAT'),
        ('aceptada', 'Aceptada por SUNAT'),
        ('observada', 'Observada por SUNAT'),
    ]
    empresa = models.ForeignKey(Company, on_delete=models.CASCADE)
    cliente_nombre = models.CharField(max_length=255)
    cliente_documento = models.CharField(max_length=20)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO, default='emitida')

class SaleItem(models.Model):
    venta = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
```

**Características:**
- Soporte para boletas y facturas
- Estados de SUNAT integrados
- Detalle de items por venta
- Cálculo automático de subtotales

### 5. Compras (Purchase & PurchaseItem)

Gestión de compras a proveedores.

```python
class Purchase(models.Model):
    empresa = models.ForeignKey(Company, on_delete=models.CASCADE)
    proveedor_nombre = models.CharField(max_length=255)
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default='registrada')

class PurchaseItem(models.Model):
    compra = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
```

**Características:**
- Registro de compras por proveedor
- Detalle de productos comprados
- Control de estados de compra

### 6. Movimientos de Inventario (InventoryMovement)

Sistema Kardex para control de inventario.

```python
class InventoryMovement(models.Model):
    MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]
    empresa = models.ForeignKey(Company, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=10, choices=MOVIMIENTO)
    referencia = models.CharField(max_length=100, blank=True)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
```

**Características:**
- Registro de entradas y salidas
- Trazabilidad completa del inventario
- Referencias para auditoría

### 7. Factura Electrónica (ElectronicInvoice)

Integración con SUNAT para facturación electrónica.

```python
class ElectronicInvoice(models.Model):
    venta = models.OneToOneField(Sale, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Company, on_delete=models.CASCADE)
    xml_enviado = models.TextField()
    cdr_respuesta = models.TextField(blank=True)
    hash = models.CharField(max_length=100)
    estado_sunat = models.CharField(max_length=20, default='pendiente')
    fecha_envio = models.DateTimeField(auto_now_add=True)
```

**Características:**
- Almacenamiento de XML enviado a SUNAT
- Respuesta CDR de SUNAT
- Hash de seguridad
- Estados de procesamiento SUNAT

## Relaciones Entre Modelos

```
Company (1) ←→ (N) User
Company (1) ←→ (N) Product
Company (1) ←→ (N) Sale
Company (1) ←→ (N) Purchase
Company (1) ←→ (N) InventoryMovement
Company (1) ←→ (N) ElectronicInvoice

Sale (1) ←→ (N) SaleItem
Purchase (1) ←→ (N) PurchaseItem
Product (1) ←→ (N) SaleItem
Product (1) ←→ (N) PurchaseItem
Product (1) ←→ (N) InventoryMovement

Sale (1) ←→ (1) ElectronicInvoice
```

## Tecnologías y Buenas Prácticas Recomendadas

### 🔐 Autenticación y Autorización
- **Djoser**: Para endpoints de autenticación (registro, login, logout, reset password)
- **JWT (Simple JWT)**: Tokens de acceso y refresh para APIs
- **Permisos por empresa**: Usuarios solo acceden a datos de su empresa
- **Roles granulares**: Admin empresa, empleado, super admin

### 🏗️ Arquitectura API
- **Django REST Framework**: API REST completa
- **Swagger/OpenAPI**: Documentación automática con drf-yasg
- **Versionado de API**: `/api/v1/` para futuras versiones
- **Paginación**: Para listas grandes de datos
- **Filtros y búsqueda**: django-filter para consultas avanzadas
- **Throttling**: Límites de requests por usuario/IP

### 📊 Base de Datos y Performance
- **PostgreSQL**: Base de datos principal (mejor para JSON, arrays)
- **Índices optimizados**: En campos de búsqueda frecuente
- **Select related/prefetch**: Optimización de queries
- **Database pooling**: Para conexiones eficientes
- **Migraciones**: Versionado de esquema de BD

### 🚀 Infraestructura y DevOps
- **Docker**: Containerización para desarrollo y producción
- **Redis**: Cache y sesiones
- **Celery**: Tareas asíncronas (envío a SUNAT, reportes)
- **AWS S3/CloudFlare**: Almacenamiento de archivos estáticos
- **Environment variables**: Configuración segura con python-decouple

### 🔒 Seguridad
- **CORS**: Configuración para frontend
- **HTTPS**: Certificados SSL en producción
- **Rate limiting**: Protección contra ataques
- **Validación de datos**: Serializers robustos
- **Logs de auditoría**: Tracking de cambios importantes

### 📱 Frontend Integration
- **API RESTful**: Endpoints consistentes y predecibles
- **JSON responses**: Formato estándar
- **Error handling**: Códigos HTTP apropiados
- **File uploads**: Para logos, imágenes de productos
- **Real-time**: WebSockets para notificaciones (opcional)

## Estructura de URLs Recomendada

```
/api/v1/auth/          # Djoser endpoints
/api/v1/companies/     # Gestión de empresas
/api/v1/users/         # Gestión de usuarios
/api/v1/products/      # Catálogo de productos
/api/v1/sales/         # Ventas y facturación
/api/v1/purchases/     # Compras
/api/v1/inventory/     # Movimientos de inventario
/api/v1/invoices/      # Facturación electrónica
/api/v1/reports/       # Reportes y analytics
/swagger/              # Documentación API
/redoc/                # Documentación alternativa
```

## Dependencias Adicionales Recomendadas

```bash
# Autenticación
pip install djoser

# Filtros y búsqueda
pip install django-filter

# CORS para frontend
pip install django-cors-headers

# Validación de datos
pip install django-phonenumber-field

# Tareas asíncronas
pip install celery redis

# Monitoreo y logs
pip install django-extensions
pip install sentry-sdk

# Testing
pip install factory-boy
pip install pytest-django
```

## Próximos Pasos de Implementación

1. **Configuración inicial**
   - Settings.py con todas las apps y middleware
   - Configuración de Djoser y JWT
   - CORS y variables de entorno

2. **Modelos y migraciones**
   - Implementar todos los modelos
   - Crear migraciones iniciales
   - Configurar admin de Django

3. **Serializers y ViewSets**
   - Serializers para cada modelo
   - ViewSets con permisos apropiados
   - Filtros y paginación

4. **URLs y documentación**
   - Configurar URLs por app
   - Swagger/OpenAPI documentation
   - Testing de endpoints

5. **Integración SUNAT**
   - Servicios para XML/SOAP
   - Validaciones específicas
   - Manejo de errores SUNAT

## Consideraciones de Seguridad SUNAT

- **Certificados digitales**: Manejo seguro de certificados
- **Validación RUC**: Verificación en tiempo real
- **Backup de XMLs**: Almacenamiento seguro de documentos
- **Logs de auditoría**: Trazabilidad completa
- **Encriptación**: Datos sensibles encriptados

---

*Esta guía será actualizada conforme avance el desarrollo del proyecto.*