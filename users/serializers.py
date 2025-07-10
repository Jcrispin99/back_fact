from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    """Serializer para crear usuarios con Djoser"""
    
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 
            'password', 'telefono', 'empresa', 'rol'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_email(self, value):
        """Validar que el email sea único"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value


class UserSerializer(BaseUserSerializer):
    """Serializer para mostrar información del usuario"""
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'telefono', 'empresa', 'empresa_nombre', 'rol', 'rol_display',
            'estado', 'is_admin', 'is_super_admin', 'date_joined',
            'fecha_creacion', 'fecha_actualizacion'
        )
        read_only_fields = (
            'id', 'date_joined', 'fecha_creacion', 'fecha_actualizacion',
            'is_admin', 'is_super_admin'
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar información del usuario"""
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'telefono', 'empresa', 'rol', 'estado'
        )
    
    def validate_rol(self, value):
        """Solo super admins pueden cambiar roles"""
        user = self.context['request'].user
        if not user.is_super_admin and 'rol' in self.initial_data:
            if self.instance.rol != value:
                raise serializers.ValidationError(
                    "No tienes permisos para cambiar el rol."
                )
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambiar contraseña"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                "Las contraseñas nuevas no coinciden."
            )
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                "La contraseña actual es incorrecta."
            )
        return value