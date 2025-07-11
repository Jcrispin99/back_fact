from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Company, Location
from .serializers import CompanySerializer, LocationSerializer
from .permissions import IsAdminOrSuperAdmin, IsCompanyOwnerOrSuperAdmin

class CompanyViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Empresas y Sucursales"""
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_empresa', 'plan_suscripcion', 'parent']
    search_fields = ['nombre', 'ruc']
    ordering_fields = ['nombre', 'fecha_registro']
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin:
            return Company.objects.filter(estado=True)
        elif user.is_admin:
            # Un admin ve su empresa y sus sucursales
            return Company.objects.filter(estado=True, id=user.empresa_id) | \
                   Company.objects.filter(estado=True, parent=user.empresa)
        return Company.objects.none() # No debería llegar aquí si los permisos son correctos

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return [permissions.IsAuthenticated(), IsCompanyOwnerOrSuperAdmin()]
        return [permissions.IsAuthenticated(), IsAdminOrSuperAdmin()]

class LocationViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Ubicaciones de las Empresas"""
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['empresa', 'es_almacen_principal']
    search_fields = ['nombre', 'direccion']
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin:
            return Location.objects.filter(estado=True)
        elif user.is_admin:
            # Un admin ve las ubicaciones de su empresa y de sus sucursales
            company_ids = [user.empresa.id] + list(user.empresa.sucursales.values_list('id', flat=True))
            return Location.objects.filter(estado=True, empresa_id__in=company_ids)
        return Location.objects.none()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return [permissions.IsAuthenticated(), IsCompanyOwnerOrSuperAdmin()]
        return [permissions.IsAuthenticated(), IsAdminOrSuperAdmin()]
