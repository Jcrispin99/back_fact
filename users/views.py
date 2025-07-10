from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import User
from .serializers import (
    UserSerializer, 
    UserUpdateSerializer, 
    ChangePasswordSerializer
)
from .permissions import IsOwnerOrAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de usuarios"""
    queryset = User.objects.filter(estado=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rol', 'empresa', 'estado']
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering_fields = ['fecha_creacion', 'email', 'first_name']
    ordering = ['-fecha_creacion']
    
    def get_queryset(self):
        """Filtrar usuarios según permisos"""
        user = self.request.user
        queryset = super().get_queryset()
        
        # Super admin ve todos los usuarios
        if user.is_super_admin:
            return queryset
        
        # Admin de empresa ve solo usuarios de su empresa
        if user.is_admin and user.empresa:
            return queryset.filter(empresa=user.empresa)
        
        # Empleados solo ven su propio perfil
        return queryset.filter(id=user.id)
    
    def get_serializer_class(self):
        """Usar diferentes serializers según la acción"""
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def perform_create(self, serializer):
        """Asignar empresa al crear usuario"""
        user = self.request.user
        
        # Si no es super admin, asignar su empresa
        if not user.is_super_admin and user.empresa:
            serializer.save(empresa=user.empresa)
        else:
            serializer.save()
    
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """Cambiar contraseña del usuario"""
        user = self.get_object()
        serializer = ChangePasswordSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            # Verificar permisos
            if request.user != user and not request.user.is_admin:
                return Response(
                    {'error': 'No tienes permisos para cambiar esta contraseña.'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response(
                {'message': 'Contraseña cambiada exitosamente.'}, 
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Activar/desactivar usuario"""
        user = self.get_object()
        
        # Solo admins pueden cambiar estado
        if not request.user.is_admin:
            return Response(
                {'error': 'No tienes permisos para cambiar el estado del usuario.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        user.estado = not user.estado
        user.save()
        
        status_text = 'activado' if user.estado else 'desactivado'
        return Response(
            {'message': f'Usuario {status_text} exitosamente.'}, 
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener información del usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Estadísticas de usuarios (solo para admins)"""
        if not request.user.is_admin:
            return Response(
                {'error': 'No tienes permisos para ver estadísticas.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        queryset = self.get_queryset()
        
        stats = {
            'total_usuarios': queryset.count(),
            'usuarios_activos': queryset.filter(estado=True).count(),
            'usuarios_inactivos': queryset.filter(estado=False).count(),
            'por_rol': {
                'admins': queryset.filter(rol='admin').count(),
                'empleados': queryset.filter(rol='empleado').count(),
                'super_admins': queryset.filter(rol='super_admin').count(),
            }
        }
        
        return Response(stats, status=status.HTTP_200_OK)
