from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin personalizado para el modelo User"""
    
    list_display = (
        'email', 'username', 'first_name', 'last_name', 
        'empresa', 'rol', 'estado', 'is_staff', 'date_joined'
    )
    list_filter = (
        'rol', 'estado', 'is_staff', 'is_superuser', 
        'empresa', 'date_joined'
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions')
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Información Personal'), {
            'fields': ('first_name', 'last_name', 'telefono')
        }),
        (_('Empresa y Rol'), {
            'fields': ('empresa', 'rol', 'estado')
        }),
        (_('Permisos'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
            'classes': ('collapse',)
        }),
        (_('Fechas Importantes'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name',
                'password1', 'password2', 'empresa', 'rol'
            ),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login', 'fecha_creacion', 'fecha_actualizacion')
    
    def get_queryset(self, request):
        """Filtrar usuarios según permisos del admin"""
        qs = super().get_queryset(request)
        
        # Super admin ve todos los usuarios
        if request.user.is_superuser:
            return qs
        
        # Admin de empresa ve solo usuarios de su empresa
        if hasattr(request.user, 'empresa') and request.user.empresa:
            return qs.filter(empresa=request.user.empresa)
        
        return qs.none()
    
    def save_model(self, request, obj, form, change):
        """Personalizar guardado del modelo"""
        # Si no es super admin, asignar su empresa
        if not request.user.is_superuser and hasattr(request.user, 'empresa'):
            if request.user.empresa and not obj.empresa:
                obj.empresa = request.user.empresa
        
        super().save_model(request, obj, form, change)
    
    def get_form(self, request, obj=None, **kwargs):
        """Personalizar formulario según permisos"""
        form = super().get_form(request, obj, **kwargs)
        
        # Si no es super admin, limitar opciones de empresa
        if not request.user.is_superuser and 'empresa' in form.base_fields:
            if hasattr(request.user, 'empresa') and request.user.empresa:
                form.base_fields['empresa'].queryset = form.base_fields['empresa'].queryset.filter(
                    id=request.user.empresa.id
                )
        
        return form
