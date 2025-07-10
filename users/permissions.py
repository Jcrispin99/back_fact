from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado que permite:
    - Lectura a usuarios autenticados
    - Escritura solo al propietario o administradores
    """
    
    def has_permission(self, request, view):
        # Permitir acceso a usuarios autenticados
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Permisos de lectura para cualquier usuario autenticado
        if request.method in permissions.SAFE_METHODS:
            # Super admin ve todo
            if request.user.is_super_admin:
                return True
            
            # Admin de empresa ve usuarios de su empresa
            if request.user.is_admin and request.user.empresa:
                return obj.empresa == request.user.empresa
            
            # Usuario ve solo su propio perfil
            return obj == request.user
        
        # Permisos de escritura
        # Super admin puede editar cualquier usuario
        if request.user.is_super_admin:
            return True
        
        # Admin de empresa puede editar usuarios de su empresa
        if request.user.is_admin and request.user.empresa:
            return obj.empresa == request.user.empresa
        
        # Usuario puede editar solo su propio perfil
        return obj == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso que permite lectura a todos los usuarios autenticados
    pero escritura solo a administradores
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsSuperAdminOnly(permissions.BasePermission):
    """
    Permiso que permite acceso solo a super administradores
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_super_admin
        )


class IsCompanyMember(permissions.BasePermission):
    """
    Permiso que verifica que el usuario pertenezca a la misma empresa
    que el objeto que está intentando acceder
    """
    
    def has_object_permission(self, request, view, obj):
        # Super admin tiene acceso a todo
        if request.user.is_super_admin:
            return True
        
        # Verificar que el usuario y el objeto pertenezcan a la misma empresa
        if hasattr(obj, 'empresa'):
            return request.user.empresa == obj.empresa
        
        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permiso que permite acceso al propietario del objeto o a administradores
    """
    
    def has_object_permission(self, request, view, obj):
        # Super admin tiene acceso a todo
        if request.user.is_super_admin:
            return True
        
        # Admin de empresa tiene acceso a objetos de su empresa
        if request.user.is_admin and request.user.empresa:
            if hasattr(obj, 'empresa'):
                return obj.empresa == request.user.empresa
            elif hasattr(obj, 'user'):
                return obj.user.empresa == request.user.empresa
        
        # Propietario del objeto
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return obj == request.user