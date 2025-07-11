#!/usr/bin/env python
"""
Script para crear datos de ejemplo en el sistema SUNAT
"""

import os
import django
from django.contrib.auth.hashers import make_password

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sunat_backend.settings')
django.setup()

from users.models import User
from companies.models import Company, Location

print("🚀 Creando datos de ejemplo...")

# 1. Crear Super Admin
print("\n👑 Creando Super Administrador...")
super_admin, created = User.objects.get_or_create(
    email='superadmin@sunat.com',
    defaults={
        'username': 'superadmin_sunat',
        'first_name': 'Super',
        'last_name': 'Administrador',
        'password': make_password('admin123'),
        'rol': 'super_admin',
        'telefono': '+51999000001',
        'estado': True
    }
)
if created:
    print(f"✅ Super Admin creado: {super_admin.email}")
else:
    print(f"ℹ️  Super Admin ya existe: {super_admin.email}")

# 2. Crear Empresas Principales
print("\n🏢 Creando empresas principales...")

empresa1, created = Company.objects.get_or_create(
    ruc='20123456789',
    defaults={
        'nombre': 'TechCorp Solutions SAC',
        'direccion': 'Av. Javier Prado Este 4200, San Isidro, Lima',
        'telefono': '+51-1-4567890',
        'email': 'contacto@techcorp.com.pe',
        'tipo_empresa': 'otros',
        'plan_suscripcion': 'premium'
    }
)
if created:
    print(f"✅ Empresa creada: {empresa1.nombre}")
else:
    print(f"ℹ️  Empresa ya existe: {empresa1.nombre}")

empresa2, created = Company.objects.get_or_create(
    ruc='20987654321',
    defaults={
        'nombre': 'Comercial Andina EIRL',
        'direccion': 'Jr. Lampa 545, Cercado de Lima, Lima',
        'telefono': '+51-1-7654321',
        'email': 'ventas@comercialandina.pe',
        'tipo_empresa': 'otros',
         'plan_suscripcion': 'basico'
    }
)
if created:
    print(f"✅ Empresa creada: {empresa2.nombre}")
else:
    print(f"ℹ️  Empresa ya existe: {empresa2.nombre}")

empresa3, created = Company.objects.get_or_create(
    ruc='20456789123',
    defaults={
        'nombre': 'Servicios Integrales del Sur SA',
        'direccion': 'Av. El Sol 123, Wanchaq, Cusco',
        'telefono': '+51-84-123456',
        'email': 'info@serviciosur.com',
        'tipo_empresa': 'otros',
         'plan_suscripcion': 'estandar'
    }
)
if created:
    print(f"✅ Empresa creada: {empresa3.nombre}")
else:
    print(f"ℹ️  Empresa ya existe: {empresa3.nombre}")

# 3. Crear Sucursales
print("\n🏪 Creando sucursales...")

sucursal1, created = Company.objects.get_or_create(
    ruc='20123456790',
    defaults={
        'nombre': 'TechCorp - Sucursal Miraflores',
        'direccion': 'Av. Larco 1301, Miraflores, Lima',
        'telefono': '+51-1-4567891',
        'email': 'miraflores@techcorp.com.pe',
        'tipo_empresa': 'otros',
        'parent': empresa1,
        'plan_suscripcion': 'premium'
    }
)
if created:
    print(f"✅ Sucursal creada: {sucursal1.nombre}")
else:
    print(f"ℹ️  Sucursal ya existe: {sucursal1.nombre}")

# 4. Crear Administradores
print("\n👨‍💼 Creando administradores...")

admin1, created = User.objects.get_or_create(
    email='admin@techcorp.com.pe',
    defaults={
        'username': 'carlos_techcorp',
        'first_name': 'Carlos',
        'last_name': 'Mendoza',
        'password': make_password('admin123'),
        'telefono': '+51999000002',
        'empresa': empresa1,
        'rol': 'admin',
        'estado': True
    }
)
if created:
    print(f"✅ Admin creado: {admin1.email} - {admin1.empresa.nombre}")
else:
    print(f"ℹ️  Admin ya existe: {admin1.email}")

admin2, created = User.objects.get_or_create(
    email='admin@comercialandina.pe',
    defaults={
        'username': 'maria_andina',
        'first_name': 'María',
        'last_name': 'García',
        'password': make_password('admin123'),
        'telefono': '+51999000003',
        'empresa': empresa2,
        'rol': 'admin',
        'estado': True
    }
)
if created:
    print(f"✅ Admin creado: {admin2.email} - {admin2.empresa.nombre}")
else:
    print(f"ℹ️  Admin ya existe: {admin2.email}")

# 5. Crear Empleados
print("\n👥 Creando empleados...")

empleado1, created = User.objects.get_or_create(
    email='juan.perez@techcorp.com.pe',
    defaults={
        'username': 'juan_perez',
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'password': make_password('empleado123'),
        'telefono': '+51999000010',
        'empresa': empresa1,
        'rol': 'empleado',
        'estado': True
    }
)
if created:
    print(f"✅ Empleado creado: {empleado1.email} - {empleado1.empresa.nombre}")
else:
    print(f"ℹ️  Empleado ya existe: {empleado1.email}")

empleado2, created = User.objects.get_or_create(
    email='pedro.silva@comercialandina.pe',
    defaults={
        'username': 'pedro_silva',
        'first_name': 'Pedro',
        'last_name': 'Silva',
        'password': make_password('empleado123'),
        'telefono': '+51999000012',
        'empresa': empresa2,
        'rol': 'empleado',
        'estado': True
    }
)
if created:
    print(f"✅ Empleado creado: {empleado2.email} - {empleado2.empresa.nombre}")
else:
    print(f"ℹ️  Empleado ya existe: {empleado2.email}")

# 6. Crear Ubicaciones
print("\n📍 Creando ubicaciones...")

ubicacion1, created = Location.objects.get_or_create(
    nombre='Almacén Principal TechCorp',
    empresa=empresa1,
    defaults={
        'direccion': 'Av. Javier Prado Este 4200 - Almacén A, San Isidro',
        'es_almacen_principal': True
    }
)
if created:
    print(f"✅ Ubicación creada: {ubicacion1.nombre} - {ubicacion1.empresa.nombre}")
else:
    print(f"ℹ️  Ubicación ya existe: {ubicacion1.nombre}")

ubicacion2, created = Location.objects.get_or_create(
    nombre='Tienda Principal Andina',
    empresa=empresa2,
    defaults={
        'direccion': 'Jr. Lampa 545 - Local 1, Cercado de Lima',
        'es_almacen_principal': False
    }
)
if created:
    print(f"✅ Ubicación creada: {ubicacion2.nombre} - {ubicacion2.empresa.nombre}")
else:
    print(f"ℹ️  Ubicación ya existe: {ubicacion2.nombre}")

# 7. Resumen final
print("\n📊 RESUMEN DE DATOS CREADOS:")
print(f"👑 Super Admins: {User.objects.filter(rol='super_admin').count()}")
print(f"👨‍💼 Administradores: {User.objects.filter(rol='admin').count()}")
print(f"👥 Empleados: {User.objects.filter(rol='empleado').count()}")
print(f"🏢 Empresas: {Company.objects.filter(parent__isnull=True).count()}")
print(f"🏪 Sucursales: {Company.objects.filter(parent__isnull=False).count()}")
print(f"📍 Ubicaciones: {Location.objects.count()}")

print("\n🔑 CREDENCIALES DE ACCESO:")
print("Super Admin: superadmin@sunat.com / admin123")
print("Admin TechCorp: admin@techcorp.com.pe / admin123")
print("Admin Andina: admin@comercialandina.pe / admin123")
print("Empleados: [email] / empleado123")

print("\n✅ ¡Datos de ejemplo creados exitosamente!")
print("🚀 Ya puedes probar el sistema con estos datos.")