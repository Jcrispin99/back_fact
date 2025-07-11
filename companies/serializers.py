from rest_framework import serializers
from .models import Company, Location


class LocationSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Location"""
    class Meta:
        model = Location
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    """Serializer para el modelo Company"""
    sucursales = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    ubicaciones = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = (
            'id', 'nombre', 'ruc', 'tipo_empresa', 'direccion', 'telefono',
            'email', 'logo_url', 'plan_suscripcion', 'estado', 'parent',
            'sucursales', 'ubicaciones'
        )