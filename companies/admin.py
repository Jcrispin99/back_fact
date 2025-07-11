from django.contrib import admin
from .models import Company, Location


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ruc', 'tipo_empresa', 'parent', 'estado')
    list_filter = ('tipo_empresa', 'estado', 'plan_suscripcion')
    search_fields = ('nombre', 'ruc')
    ordering = ('nombre',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa', 'es_almacen_principal', 'estado')
    list_filter = ('empresa', 'es_almacen_principal', 'estado')
    search_fields = ('nombre', 'empresa__nombre')
    ordering = ('empresa', 'nombre')
