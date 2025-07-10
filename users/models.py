from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('super_admin', 'Super Administrador'),
    ]
    
    email = models.EmailField(unique=True)
    empresa = models.ForeignKey(
        'companies.Company', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='usuarios'
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='empleado')
    estado = models.BooleanField(default=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    @property
    def is_admin(self):
        return self.rol == 'admin' or self.rol == 'super_admin'
    
    @property
    def is_super_admin(self):
        return self.rol == 'super_admin'
