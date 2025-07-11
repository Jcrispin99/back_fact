from django.db import models


class Company(models.Model):
    TIPO_EMPRESA_CHOICES = [
        ('farmacia', 'Farmacia'),
        ('ropa', 'Tienda de Ropa'),
        ('abarrotes', 'Tienda de Abarrotes'),
        ('restaurante', 'Restaurante'),
        ('otros', 'Otros'),
    ]
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sucursales',
        verbose_name='Empresa Principal'
    )
    nombre = models.CharField(max_length=255)
    ruc = models.CharField(max_length=11, unique=True)
    tipo_empresa = models.CharField(max_length=20, choices=TIPO_EMPRESA_CHOICES)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    logo_url = models.URLField(blank=True)
    plan_suscripcion = models.CharField(max_length=20, default="free")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return self.nombre


class Location(models.Model):
    empresa = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='ubicaciones'
    )
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, blank=True)
    es_almacen_principal = models.BooleanField(default=False)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
        unique_together = ('empresa', 'nombre')

    def __str__(self):
        return f"{self.nombre} ({self.empresa.nombre})"
