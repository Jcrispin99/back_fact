from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Router para ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Endpoints de Djoser para autenticación
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
    # Endpoints personalizados de usuarios
    path('', include(router.urls)),
]