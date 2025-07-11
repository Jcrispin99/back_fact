from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdminUser(BasePermission):
    """
    Allows access only to super admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_super_admin

class IsAdminOrSuperAdmin(BasePermission):
    """
    Allows access to admin or super admin users.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_admin or request.user.is_super_admin

class IsCompanyOwnerOrSuperAdmin(BasePermission):
    """
    Object-level permission to only allow owners of an object to view/edit it,
    or superadmins to do anything.
    Assumes the model instance has an `empresa` attribute or is a Company.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Superadmins can do anything
        if request.user.is_super_admin:
            return True

        # Admins can interact with objects related to their company
        if request.user.is_admin:
            from companies.models import Company
            # The object is a Company instance
            if isinstance(obj, Company):
                # An admin can only interact with their own company or its branches
                return obj == request.user.empresa or obj.parent == request.user.empresa
            # The object is a Location instance or other model with 'empresa'
            elif hasattr(obj, 'empresa'):
                return obj.empresa == request.user.empresa
        
        return False