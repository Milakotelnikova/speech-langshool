from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'courses'

# Настройка роутера для ViewSets
router = DefaultRouter()
router.register(r'teachers', views.TeacherViewSet)
router.register(r'categories', views.CourseCategoryViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'user-lessons', views.UserLessonsViewSet, basename='user-lessons')


urlpatterns = [
    # Маршруты для ViewSets
    path('', include(router.urls)),
    
    # Маршруты для занятий
    path('lessons/', views.LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson-detail'),
    
    # Маршруты для записей на занятия
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/<int:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment-detail'),

] 