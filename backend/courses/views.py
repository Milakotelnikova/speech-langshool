import time

from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample

from .models import Teacher, CourseCategory, Course, Lesson, Enrollment
from .serializers import (
    TeacherSerializer, CourseCategorySerializer, CourseSerializer,
    LessonSerializer, SimpleLessonSerializer, EnrollmentSerializer,
    CourseDetailSerializer, UserLessonSerializer
)


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра преподавателей"""
    
    queryset = Teacher.objects.filter(is_active=True)
    serializer_class = TeacherSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CourseCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра категорий курсов"""
    
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slugzzz'


@extend_schema_view(
    list=extend_schema(
        summary="Список курсов",
        description="Получить список всех активных курсов.",
        tags=["Курсы"]
    ),
    retrieve=extend_schema(
        summary="Детальная информация о курсе",
        description="Получить подробную информацию о конкретном курсе.",
        tags=["Курсы"]
    )
)
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра курсов"""
    
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category__name']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer
    
    @extend_schema(
        summary="Курсы по категории",
        description="Получить список курсов, относящихся к определенной категории.",
        parameters=[
            OpenApiParameter(
                name="slug",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Слаг категории курсов"
            )
        ],
        tags=["Курсы"],
        examples=[
            OpenApiExample(
                "Пример ответа",
                summary="Курсы категории",
                value=[{
                    "id": 1,
                    "name": "Ораторское мастерство",
                    "slug": "oratorskoe-masterstvo",
                    "description": "Базовый курс ораторского мастерства",
                    "category": {
                        "id": 1,
                        "name": "Ораторское искусство",
                        "slug": "oratorskoe-iskusstvo"
                    },
                    "duration": 8,
                    "price": "5000.00",
                    "image": "http://example.com/media/courses/images/oratorskoe.jpg"
                }]
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Получить курсы по категории"""
        category_slug = request.query_params.get('slug', None)
        
        if not category_slug:
            return Response(
                {"detail": _("Необходимо указать slug категории.")},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        category = get_object_or_404(CourseCategory, slug=category_slug)
        courses = self.queryset.filter(category=category)
        
        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Курсы по возрастной группе",
        description="Получить список курсов для определенной возрастной группы.",
        parameters=[
            OpenApiParameter(
                name="group",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Код возрастной группы (children, teens, adults, seniors, all)",
                enum=["children", "teens", "adults", "seniors", "all"]
            )
        ],
        tags=["Курсы"]
    )
    @action(detail=False, methods=['get'])
    def by_age_group(self, request):
        """Получить курсы по возрастной группе"""
        age_group = request.query_params.get('group', None)
        
        if not age_group or age_group not in dict(Course.AGE_CHOICES):
            return Response(
                {"detail": _("Необходимо указать корректную возрастную группу.")},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        courses = self.queryset.filter(Q(age_group=age_group) | Q(age_group='all'))
        
        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)



class UserLessonsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserLessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        subscribed_courses = Course.objects.filter(subscriptions__user=user)
        return Lesson.objects.filter(course__in=subscribed_courses)



class LessonListView(generics.ListAPIView):
    """View для просмотра списка занятий"""
    
    serializer_class = SimpleLessonSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'course__name']
    
    def get_queryset(self):
        queryset = Lesson.objects.filter(course__is_active=True)
        
        # Фильтр по курсу
        course_slug = self.request.query_params.get('course', None)
        if course_slug:
            queryset = queryset.filter(course__slug=course_slug)
        
        # Фильтр по преподавателю
        teacher_id = self.request.query_params.get('teacher', None)
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        
        return queryset


class LessonDetailView(generics.RetrieveAPIView):
    """View для просмотра детальной информации о занятии"""
    
    queryset = Lesson.objects.filter(course__is_active=True)
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]


class EnrollmentListView(generics.ListCreateAPIView):
    """View для просмотра и создания записей на занятия"""
    
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)




class EnrollmentDetailView(generics.RetrieveDestroyAPIView):
    """View для просмотра и отмены записи на занятие"""

    serializer_class = EnrollmentSerializer

    def get_permissions(self):
        if self.request.method == 'OPTIONS':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        start = time.time()
        instance = self.get_object()
        
        if instance.status == 'confirmed':
            self.perform_destroy(instance)
            duration = time.time() - start
            print("Confirmed cancel took", duration)
            return Response({"detail": _("Запись успешно отменена.")}, status=200)
        
        self.perform_destroy(instance)
        duration = time.time() - start
        print("Pending cancel took", duration)
        return Response({"detail": _("Запись успешно удалена.")}, status=204)