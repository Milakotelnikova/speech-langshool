from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, CourseCategory
from .models import Application


class ApplicationModelTest(TestCase):
    """Тесты для модели Application"""
    
    def setUp(self):
        # Создаем категорию и курс
        self.category = CourseCategory.objects.create(
            name='Китайский язык',
            slug='chinese',
            description='Курсы китайского языка'
        )
        
        self.course = Course.objects.create(
            name='Китайский для начинающих',
            slug='chinese-beginners',
            description='Базовый курс китайского языка',
            category=self.category,
            age_group='adults',
            format='offline',
            price=5500,
            duration=40
        )
        
        # Создаем заявку
        self.application = Application.objects.create(
            name='Иван Иванов',
            phone='1234567890',
            email='ivan@example.com',
            child_age=8,
            course=self.course,
            message='Интересует китайский для ребенка',
            status='new'
        )
    
    def test_application_creation(self):
        """Тест создания заявки"""
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(self.application.name, 'Иван Иванов')
        self.assertEqual(self.application.email, 'ivan@example.com')
        self.assertEqual(self.application.course, self.course)
        self.assertEqual(self.application.status, 'new')
    
    def test_application_str_method(self):
        """Тест метода __str__ модели заявки"""
        self.assertEqual(str(self.application), 'Иван Иванов - ivan@example.com (Новая)')



class ApplicationAPITest(APITestCase):
    """Тесты для API заявок"""
    
    def setUp(self):
        # Создаем категорию и курс
        self.category = CourseCategory.objects.create(
            name='Арабский язык',
            slug='arabic',
            description='Курсы арабского языка'
        )
        
        self.course = Course.objects.create(
            name='Арабский для начинающих',
            slug='arabic-beginners',
            description='Базовый курс арабского языка',
            category=self.category,
            age_group='adults',
            format='offline',
            price=6000,
            duration=50
        )
        
        # URL для создания заявки
        self.create_application_url = reverse('applications:application-create')
        
        # Данные для заявки
        self.application_data = {
            'name': 'Алексей Сидоров',
            'phone': '1234567890',
            'email': 'alex@example.com',
            'child_age': 10,
            'course_id': self.course.id,
            'message': 'Интересует курс арабского для ребенка'
        }
    
    def test_create_application(self):
        """Тест создания заявки через API"""
        response = self.client.post(self.create_application_url, self.application_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        
        application = Application.objects.first()
        self.assertEqual(application.name, 'Алексей Сидоров')
        self.assertEqual(application.email, 'alex@example.com')
        self.assertEqual(application.course, self.course)
        self.assertEqual(application.status, 'new')
    
    def test_create_application_without_course(self):
        """Тест создания заявки без указания курса"""
        self.application_data.pop('course_id')
        response = self.client.post(self.create_application_url, self.application_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        
        application = Application.objects.first()
        self.assertEqual(application.name, 'Алексей Сидоров')
        self.assertEqual(application.email, 'alex@example.com')
        self.assertIsNone(application.course)

