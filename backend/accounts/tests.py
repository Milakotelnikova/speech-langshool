from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User, Child


class UserModelTest(TestCase):
    """Тесты для модели User"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            name='Test',
        )
    
    def test_user_creation(self):
        """Тест создания пользователя"""
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.name, 'Test')
        self.assertTrue(self.user.check_password('testpassword123'))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
    
    def test_user_str_method(self):
        """Тест метода __str__ модели пользователя"""
        self.assertEqual(str(self.user), 'Test User <test@example.com>')
        
    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword123',
            name='Admin',
        )
        
        self.assertEqual(User.objects.count(), 2)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class ChildModelTest(TestCase):
    """Тесты для модели Child"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='parent@example.com',
            password='testpassword123',
            name='Parent',
            is_parent=True
        )
        
        self.child = Child.objects.create(
            parent=self.user,
            name='Child',
            age=8
        )
    
    def test_child_creation(self):
        """Тест создания ребенка"""
        self.assertEqual(Child.objects.count(), 1)
        self.assertEqual(self.child.parent, self.user)
        self.assertEqual(self.child.name, 'Child')
        self.assertEqual(self.child.age, 8)
    
    def test_child_str_method(self):
        """Тест метода __str__ модели ребенка"""
        self.assertEqual(str(self.child), 'Child User (8)')
    
    def test_related_name(self):
        """Тест связи parent-children"""
        self.assertEqual(self.user.children.count(), 1)
        self.assertEqual(self.user.children.first(), self.child)


class UserRegistrationAPITest(APITestCase):
    """Тесты для API регистрации пользователя"""
    
    def setUp(self):
        self.url = reverse('accounts:register')
        self.user_data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'password_confirm': 'newpassword123',
            'name': 'New',
            'phone': '1234567890'
        }
    
    def test_user_registration_success(self):
        """Тест успешной регистрации пользователя"""
        response = self.client.post(self.url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        
        user = User.objects.get(email='newuser@example.com')
        self.assertEqual(user.name, 'New')
        self.assertEqual(user.phone, '1234567890')
    
    def test_user_registration_with_invalid_email(self):
        """Тест регистрации пользователя с невалидным email"""
        self.user_data['email'] = 'invalid-email'
        response = self.client.post(self.url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(User.objects.count(), 0)
    
    def test_user_registration_with_short_password(self):
        """Тест регистрации пользователя с коротким паролем"""
        self.user_data['password'] = 'short'
        self.user_data['password_confirm'] = 'short'
        response = self.client.post(self.url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(User.objects.count(), 0)


class LoginLogoutAPITest(APITestCase):
    """Тесты для API входа и выхода пользователя"""
    
    def setUp(self):
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            name='Test',
        )
    
    def test_login_success(self):
        """Тест успешного входа пользователя"""
        response = self.client.post(
            self.login_url, 
            {'email': 'testuser@example.com', 'password': 'testpassword123'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'testuser@example.com')
    
    def test_login_with_wrong_password(self):
        """Тест входа с неверным паролем"""
        response = self.client.post(
            self.login_url, 
            {'email': 'testuser@example.com', 'password': 'wrongpassword'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_with_non_existent_email(self):
        """Тест входа с несуществующим email"""
        response = self.client.post(
            self.login_url, 
            {'email': 'nonexistent@example.com', 'password': 'testpassword123'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_logout(self):
        """Тест выхода пользователя"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

