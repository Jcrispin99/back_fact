from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Company, Location

User = get_user_model()

class MainCompanyAPITests(APITestCase):
    """Tests para empresas principales"""
    
    def setUp(self):
        # Crear super administrador
        self.superadmin_user = User.objects.create_user(
            username='superadmin',
            email='superadmin@example.com',
            password='password123',
            rol='super_admin',
            first_name='Super',
            last_name='Admin'
        )
        
        # Crear empresa principal
        self.main_company = Company.objects.create(
            nombre='Empresa Principal Test',
            ruc='12345678901',
            tipo_empresa='farmacia',
            direccion='Av. Principal 123',
            telefono='987654321',
            email='empresa@test.com'
        )
        
        # Crear administrador de empresa
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password123',
            rol='admin',
            empresa=self.main_company,
            first_name='Admin',
            last_name='User'
        )
        
        # Crear otra empresa para tests de aislamiento
        self.other_company = Company.objects.create(
            nombre='Otra Empresa',
            ruc='10987654321',
            tipo_empresa='ropa'
        )

    def test_superadmin_can_list_all_companies(self):
        """Super admin puede ver todas las empresas"""
        self.client.force_authenticate(user=self.superadmin_user)
        url = reverse('company-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_admin_can_list_only_own_company(self):
        """Admin solo puede ver su propia empresa"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('company-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nombre'], self.main_company.nombre)

    def test_admin_cannot_see_other_company_details(self):
        """Admin no puede ver detalles de otras empresas"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('company-detail', kwargs={'pk': self.other_company.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_update_own_company(self):
        """Admin puede actualizar su propia empresa"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('company-detail', kwargs={'pk': self.main_company.pk})
        data = {
            'nombre': 'Empresa Principal Actualizada',
            'ruc': '12345678901',
            'tipo_empresa': 'farmacia'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.main_company.refresh_from_db()
        self.assertEqual(self.main_company.nombre, 'Empresa Principal Actualizada')


class BranchAPITests(APITestCase):
    """Tests para sucursales"""
    
    def setUp(self):
        # Crear empresa principal
        self.main_company = Company.objects.create(
            nombre='Empresa Principal para Sucursales',
            ruc='99887766554',
            tipo_empresa='abarrotes'
        )
        
        # Crear administrador
        self.admin_user = User.objects.create_user(
            username='branchadmin',
            email='branchadmin@example.com',
            password='password123',
            rol='admin',
            empresa=self.main_company,
            first_name='Branch',
            last_name='Admin'
        )

    def test_admin_can_create_branch_for_own_company(self):
        """Admin puede crear sucursal para su empresa"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('company-list')
        data = {
            'nombre': 'Sucursal Norte',
            'ruc': '99887766553',
            'tipo_empresa': 'abarrotes',
            'parent': self.main_company.id,
            'direccion': 'Av. Norte 456'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)  # Principal + sucursal
        branch = Company.objects.get(ruc='99887766553')
        self.assertEqual(branch.parent, self.main_company)

    def test_admin_can_list_own_company_and_branches(self):
        """Admin puede listar su empresa y sus sucursales"""
        self.client.force_authenticate(user=self.admin_user)
        
        # Crear sucursal
        branch = Company.objects.create(
            nombre='Sucursal Sur',
            ruc='99887766552',
            tipo_empresa='abarrotes',
            parent=self.main_company
        )
        
        url = reverse('company-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Principal + sucursal
        
        company_names = {c['nombre'] for c in response.data['results']}
        self.assertIn(self.main_company.nombre, company_names)
        self.assertIn(branch.nombre, company_names)

    def test_admin_can_update_own_branch(self):
        """Admin puede actualizar sus sucursales"""
        self.client.force_authenticate(user=self.admin_user)
        
        # Crear sucursal
        branch = Company.objects.create(
            nombre='Sucursal Este',
            ruc='99887766551',
            tipo_empresa='abarrotes',
            parent=self.main_company
        )
        
        url = reverse('company-detail', kwargs={'pk': branch.pk})
        data = {
            'nombre': 'Sucursal Este Actualizada',
            'direccion': 'Nueva dirección'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        branch.refresh_from_db()
        self.assertEqual(branch.nombre, 'Sucursal Este Actualizada')


class LocationAPITests(APITestCase):
    """Tests para ubicaciones"""
    
    def setUp(self):
        # Crear empresa
        self.company = Company.objects.create(
            nombre='Empresa para Ubicaciones',
            ruc='22334455667',
            tipo_empresa='restaurante'
        )
        
        # Crear administrador
        self.admin_user = User.objects.create_user(
            username='locationadmin',
            email='locationadmin@example.com',
            password='password123',
            rol='admin',
            empresa=self.company,
            first_name='Location',
            last_name='Admin'
        )
        
        # Crear super admin
        self.superadmin_user = User.objects.create_user(
            username='superadmin2',
            email='superadmin2@example.com',
            password='password123',
            rol='super_admin'
        )

    def test_admin_can_create_location_for_own_company(self):
        """Admin puede crear ubicación para su empresa"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('location-list')
        data = {
            'nombre': 'Almacén Principal',
            'empresa': self.company.id,
            'direccion': 'Calle Almacén 123',
            'es_almacen_principal': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)
        location = Location.objects.get()
        self.assertEqual(location.empresa, self.company)
        self.assertTrue(location.es_almacen_principal)

    def test_admin_can_list_locations_for_own_company(self):
        """Admin puede listar ubicaciones de su empresa"""
        self.client.force_authenticate(user=self.admin_user)
        
        # Crear ubicaciones
        Location.objects.create(
            nombre='Almacén Norte',
            empresa=self.company,
            direccion='Norte 123'
        )
        Location.objects.create(
            nombre='Almacén Sur',
            empresa=self.company,
            direccion='Sur 456'
        )
        
        url = reverse('location-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_superadmin_can_see_all_locations(self):
        """Super admin puede ver todas las ubicaciones"""
        self.client.force_authenticate(user=self.superadmin_user)
        
        # Crear otra empresa y ubicación
        other_company = Company.objects.create(
            nombre='Otra Empresa',
            ruc='11223344556',
            tipo_empresa='otros'
        )
        Location.objects.create(
            nombre='Ubicación Empresa 1',
            empresa=self.company
        )
        Location.objects.create(
            nombre='Ubicación Empresa 2',
            empresa=other_company
        )
        
        url = reverse('location-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_admin_can_update_own_location(self):
        """Admin puede actualizar ubicaciones de su empresa"""
        self.client.force_authenticate(user=self.admin_user)
        
        location = Location.objects.create(
            nombre='Ubicación Original',
            empresa=self.company,
            direccion='Dirección Original'
        )
        
        url = reverse('location-detail', kwargs={'pk': location.pk})
        data = {
            'nombre': 'Ubicación Actualizada',
            'direccion': 'Nueva Dirección'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        location.refresh_from_db()
        self.assertEqual(location.nombre, 'Ubicación Actualizada')
        self.assertEqual(location.direccion, 'Nueva Dirección')


class PermissionsTests(APITestCase):
    """Tests específicos para permisos"""
    
    def setUp(self):
        # Crear empresa
        self.company = Company.objects.create(
            nombre='Empresa Test Permisos',
            ruc='55566677788',
            tipo_empresa='farmacia'
        )
        
        # Crear empleado (sin permisos de admin)
        self.employee_user = User.objects.create_user(
            username='employee',
            email='employee@example.com',
            password='password123',
            rol='empleado',
            empresa=self.company
        )

    def test_employee_cannot_access_companies(self):
        """Empleado no puede acceder a endpoints de empresas"""
        self.client.force_authenticate(user=self.employee_user)
        url = reverse('company-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_cannot_access_locations(self):
        """Empleado no puede acceder a endpoints de ubicaciones"""
        self.client.force_authenticate(user=self.employee_user)
        url = reverse('location-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_access(self):
        """Usuario no autenticado no puede acceder"""
        url = reverse('company-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
