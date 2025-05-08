from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User, Child
from .models import Teacher, CourseCategory, Course, Lesson, Enrollment


class CourseCategoryModelTest(TestCase):
    """Тесты для модели CourseCategory"""
    
    def setUp(self):
        self.category = CourseCategory.objects.create(
            name='Английский язык',
            slug='english',
            description='Курсы английского языка'
        )
    
    def test_category_creation(self):
        """Тест создания категории курса"""
        self.assertEqual(CourseCategory.objects.count(), 1)
        self.assertEqual(self.category.name, 'Английский язык')
        self.assertEqual(self.category.slug, 'english')
    
    def test_category_str_method(self):
        """Тест метода __str__ модели категории"""
        self.assertEqual(str(self.category), 'Английский язык')


class CourseModelTest(TestCase):
    """Тесты для модели Course"""
    
    def setUp(self):
        self.category = CourseCategory.objects.create(
            name='Испанский язык',
            slug='spanish',
            description='Курсы испанского языка'
        )
        
        self.course = Course.objects.create(
            name='Испанский для начинающих',
            slug='spanish-beginners',
            description='Базовый курс испанского языка',
            category=self.category,
            age_group='adults',
            format='offline',
            price=5000,
            duration=40
        )
    
    def test_course_creation(self):
        """Тест создания курса"""
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(self.course.name, 'Испанский для начинающих')
        self.assertEqual(self.course.category, self.category)
        self.assertEqual(self.course.price, 5000)
    
    def test_course_str_method(self):
        """Тест метода __str__ модели курса"""
        self.assertEqual(str(self.course), 'Испанский для начинающих')


class TeacherModelTest(TestCase):
    """Тесты для модели Teacher"""
    
    def setUp(self):
        self.teacher = Teacher.objects.create(
            name='Иван',
            bio='Опытный преподаватель',
            email='teacher@example.com',
            phone='1234567890'
        )
    
    def test_teacher_creation(self):
        """Тест создания преподавателя"""
        self.assertEqual(Teacher.objects.count(), 1)
        self.assertEqual(self.teacher.name, 'Иван')
        self.assertEqual(self.teacher.email, 'teacher@example.com')
    
    def test_teacher_str_method(self):
        """Тест метода __str__ модели преподавателя"""
        self.assertEqual(str(self.teacher), 'Иван Петров')


class LessonModelTest(TestCase):
    """Тесты для модели Lesson"""
    
    def setUp(self):
        self.category = CourseCategory.objects.create(
            name='Немецкий язык',
            slug='german',
            description='Курсы немецкого языка'
        )
        
        self.course = Course.objects.create(
            name='Немецкий для начинающих',
            slug='german-beginners',
            description='Базовый курс немецкого языка',
            category=self.category,
            age_group='adults',
            format='offline',
            price=5500,
            duration=45
        )
        
        self.teacher = Teacher.objects.create(
            name='Ольга',
            bio='Преподаватель немецкого'
        )
        
        start_time = timezone.now() + timedelta(days=1)
        self.lesson = Lesson.objects.create(
            name='Введение в немецкий',
            course=self.course,
            teacher=self.teacher,
            description='Вводное занятие',
            start_time=start_time,
            end_time=start_time + timedelta(hours=2),
            location='Аудитория 101',
            max_students=10
        )
    
    def test_lesson_creation(self):
        """Тест создания занятия"""
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(self.lesson.name, 'Введение в немецкий')
        self.assertEqual(self.lesson.course, self.course)
        self.assertEqual(self.lesson.teacher, self.teacher)
        self.assertEqual(self.lesson.max_students, 10)
    
    def test_lesson_properties(self):
        """Тест свойств модели занятия"""
        self.assertFalse(self.lesson.is_full)
        self.assertEqual(self.lesson.available_seats, 10)


class EnrollmentModelTest(TestCase):
    """Тесты для модели Enrollment"""
    
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(
            email='student@example.com',
            password='testpassword123',
            name='Студент',
        )
        
        # Создаем ребенка для пользователя
        self.child = Child.objects.create(
            parent=self.user,
            name='Ребенок',
            age=12
        )
        
        # Создаем категорию
        self.category = CourseCategory.objects.create(
            name='Французский язык',
            slug='french',
            description='Курсы французского языка'
        )
        
        # Создаем курс
        self.course = Course.objects.create(
            name='Французский для детей',
            slug='french-kids',
            description='Курс французского для детей',
            category=self.category,
            age_group='kids',
            format='offline',
            price=4500,
            duration=30
        )
        
        # Создаем преподавателя
        self.teacher = Teacher.objects.create(
            name='Мария',
            bio='Преподаватель французского'
        )
        
        # Создаем занятие
        start_time = timezone.now() + timedelta(days=2)
        self.lesson = Lesson.objects.create(
            name='Приветствия на французском',
            course=self.course,
            teacher=self.teacher,
            description='Учим приветствия',
            start_time=start_time,
            end_time=start_time + timedelta(hours=1.5),
            location='Аудитория 102',
            max_students=8
        )
        
        # Создаем запись на занятие
        self.enrollment = Enrollment.objects.create(
            user=self.user,
            child=self.child,
            lesson=self.lesson,
            status='confirmed'
        )
    
    def test_enrollment_creation(self):
        """Тест создания записи на занятие"""
        self.assertEqual(Enrollment.objects.count(), 1)
        self.assertEqual(self.enrollment.user, self.user)
        self.assertEqual(self.enrollment.child, self.child)
        self.assertEqual(self.enrollment.lesson, self.lesson)
        self.assertEqual(self.enrollment.status, 'confirmed')
    
    def test_enrollment_str_method(self):
        """Тест метода __str__ модели записи на занятие"""
        expected = f"Ребенок - {self.lesson.name} (Подтверждено)"
        self.assertEqual(str(self.enrollment), expected)
    
    def test_lesson_available_seats_after_enrollment(self):
        """Тест свойства available_seats после записи на занятие"""
        self.assertEqual(self.lesson.available_seats, 7)
        self.assertFalse(self.lesson.is_full)


class CourseAPITest(APITestCase):
    """Тесты для API курсов"""
    
    def setUp(self):
        # Создаем категорию
        self.category = CourseCategory.objects.create(
            name='Итальянский язык',
            slug='italian',
            description='Курсы итальянского языка'
        )
        
        # Создаем курс
        self.course = Course.objects.create(
            name='Итальянский для путешественников',
            slug='italian-travel',
            description='Курс итальянского для путешествий',
            category=self.category,
            age_group='adults',
            format='hybrid',
            price=6000,
            duration=25
        )
        
        # URL для списка курсов
        self.courses_url = reverse('courses:course-list')
        
        # URL для деталей курса
        self.course_detail_url = reverse('courses:course-detail', kwargs={'slug': self.course.slug})
    
    def test_get_courses_list(self):
        """Тест получения списка курсов"""
        response = self.client.get(self.courses_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Проверяем пагинированный ответ
        self.assertIn('results', response.data)
        
        # Проверяем, что наш курс в результатах
        course_found = False
        for course in response.data['results']:
            if course['name'] == 'Итальянский для путешественников':
                course_found = True
                break
        
        self.assertTrue(course_found, "Созданный курс не найден в результатах API")
    
    def test_get_course_detail(self):
        """Тест получения деталей курса"""
        response = self.client.get(self.course_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Итальянский для путешественников')
        self.assertEqual(response.data['category']['name'], 'Итальянский язык')
        self.assertEqual(response.data['price'], '6000.00')


class LessonAPITest(APITestCase):
    """Тесты для API занятий"""
    
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(
            email='student@example.com',
            password='testpassword123',
            name='Студент',
        )
        
        # Создаем ребенка для пользователя
        self.child = Child.objects.create(
            parent=self.user,
            name='Ребенок',
            age=12
        )
        
        # Авторизуем пользователя
        self.client.force_authenticate(user=self.user)
        
        # Создаем категорию
        self.category = CourseCategory.objects.create(
            name='Японский язык',
            slug='japanese',
            description='Курсы японского языка'
        )
        
        # Создаем курс
        self.course = Course.objects.create(
            name='Японский для начинающих',
            slug='japanese-beginners',
            description='Базовый курс японского языка',
            category=self.category,
            age_group='adults',
            format='online',
            price=7000,
            duration=60
        )
        
        # Создаем преподавателя
        self.teacher = Teacher.objects.create(
            name='Елена',
            bio='Преподаватель японского'
        )
        
        # Создаем занятие
        start_time = timezone.now() + timedelta(days=3)
        self.lesson = Lesson.objects.create(
            name='Японский алфавит',
            course=self.course,
            teacher=self.teacher,
            description='Изучение хираганы и катаканы',
            start_time=start_time,
            end_time=start_time + timedelta(hours=2),
            location='Zoom',
            max_students=15
        )
        
        # URL для списка занятий
        self.lessons_url = reverse('courses:lesson-list')
        
        # URL для деталей занятия
        self.lesson_detail_url = reverse('courses:lesson-detail', kwargs={'pk': self.lesson.pk})
        
        # URL для записи на занятие
        self.enrollment_url = reverse('courses:enrollment-list')
    
    def test_get_lessons_list(self):
        """Тест получения списка занятий"""
        response = self.client.get(self.lessons_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Проверяем пагинированный ответ
        self.assertIn('results', response.data)
        
        # Проверяем, что наш урок в результатах
        lesson_found = False
        for lesson in response.data['results']:
            if lesson['name'] == 'Японский алфавит':
                lesson_found = True
                break
        
        self.assertTrue(lesson_found, "Созданный урок не найден в результатах API")
    
    def test_enroll_to_lesson(self):
        """Тест записи на занятие"""
        enrollment_data = {
            'lesson_id': self.lesson.id,
            'child_id': self.child.id
        }
        
        response = self.client.post(self.enrollment_url, enrollment_data, format='json')
        
        # Проверяем ответ
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Проверяем, что запись создана
        self.assertEqual(Enrollment.objects.count(), 1)
        
        enrollment = Enrollment.objects.first()
        self.assertEqual(enrollment.user, self.user)
        self.assertEqual(enrollment.child, self.child)
        self.assertEqual(enrollment.lesson, self.lesson)
