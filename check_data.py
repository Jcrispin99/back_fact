#!/usr/bin/env python
"""
Script para verificar los datos creados
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sunat_backend.settings')
django.setup()

from users.models import User
from companies.models import Company, Location

print("=== RESUMEN DE DATOS CREADOS ===")
print(f"👥 Total Usuarios: {User.objects.count()}")
print(f"🏢 Total Empresas: {Company.objects.count()}")
print(f"📍 Total Ubicaciones: {Location.objects.count()}")

print("\n=== EMPRESAS CREADAS ===")
for empresa in Company.objects.all():
    parent_info = f" (Sucursal de: {empresa.parent.nombre})" if empresa.parent else " (Principal)"
    print(f"- {empresa.nombre} (RUC: {empresa.ruc}){parent_info}")

print("\n=== USUARIOS POR ROL ===")
print(f"👑 Super Admins: {User.objects.filter(rol='super_admin').count()}")
print(f"👨‍💼 Administradores: {User.objects.filter(rol='admin').count()}")
print(f"👥 Empleados: {User.objects.filter(rol='empleado').count()}")

print("\n=== DETALLE DE USUARIOS ===")
for user in User.objects.all():
    empresa_info = user.empresa.nombre if user.empresa else "Sin empresa"
    print(f"- {user.email} ({user.rol}) - {empresa_info}")

print("\n=== UBICACIONES ===")
for ubicacion in Location.objects.all():
    tipo_info = "Almacén Principal" if ubicacion.es_almacen_principal else "Ubicación"
    print(f"- {ubicacion.nombre} ({tipo_info}) - {ubicacion.empresa.nombre}")

print("\n=== CREDENCIALES DE ACCESO ===")
print("🔑 Para probar el sistema, puedes usar:")
print("Super Admin: superadmin@sunat.com / admin123")
print("Admin TechCorp: admin@techcorp.com.pe / admin123")
print("Admin Andina: admin@comercialandina.pe / admin123")
print("Empleado TechCorp: juan.perez@techcorp.com.pe / empleado123")
print("Empleado Andina: pedro.silva@comercialandina.pe / empleado123")

print("\n✅ ¡Datos verificados correctamente!")