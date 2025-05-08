from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from .models import Teacher, CourseCategory, Course, Lesson, Enrollment
from accounts.models import Child
from accounts.serializers import UserSerializer, ChildSerializer


class TeacherSerializer(serializers.ModelSerializer):
    """Сериализатор для модели преподавателя"""
    
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'bio', 'photo', 'email', 'phone']


class CourseCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории курса"""
    
    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'slug', 'description']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Пример курса',
            summary='Основная информация о курсе',
            description='Содержит всю базовую информацию о курсе',
            value={
                'id': 1,
                'name': 'Ораторское мастерство',
                'slug': 'oratorskoe-masterstvo',
                'description': 'Курс для развития навыков публичных выступлений',
                'category': {
                    'id': 1,
                    'name': 'Ораторское искусство',
                    'slug': 'oratorskoe-iskusstvo',
                    'description': 'Курсы по ораторскому искусству'
                },
                'age_group': 'adults',
                'format': 'offline',
                'price': '5000.00',
                'duration': 8,
                'image': 'http://example.com/media/courses/oratorskoe.jpg',
                'is_active': True
            }
        )
    ]
)
class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курса"""
    
    category = CourseCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=CourseCategory.objects.all(),
        source='category',
        write_only=True
    )
    
    class Meta:
        model = Course
        fields = [
            'id', 'name', 'slug', 'description', 'category', 'category_id',
            'age_group', 'format', 'price', 'duration', 'image', 'is_active'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SimpleLessonSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для модели занятия без вложенных объектов"""
    
    teacher_name = serializers.SerializerMethodField()
    is_full = serializers.BooleanField(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'name', 'course', 'teacher_name', 'description',
            'start_time', 'end_time', 'location', 'max_students',
            'is_full', 'available_seats',
        ]
    
    def get_teacher_name(self, obj):
        return f"{obj.teacher.name}"


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели занятия"""
    
    teacher = TeacherSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        source='teacher',
        write_only=True
    )
    
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source='course',
        write_only=True
    )
    
    is_full = serializers.BooleanField(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'name', 'course', 'course_id', 'teacher', 'teacher_id',
            'description', 'start_time', 'end_time', 'location', 'max_students',
            'is_full', 'available_seats',
        ]
        read_only_fields = ['created_at', 'updated_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    """Сериализатор для записи на занятие"""
    
    user = UserSerializer(read_only=True)
    child = ChildSerializer(read_only=True)
    child_id = serializers.PrimaryKeyRelatedField(
        queryset=Child.objects.all(),
        source='child',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    lesson = SimpleLessonSerializer(read_only=True)
    lesson_id = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(),
        source='lesson',
        write_only=True
    )
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'user', 'child', 'child_id', 'lesson', 'lesson_id',
            'status', 'created_at'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        # Проверяем, что занятие не заполнено
        lesson = attrs.get('lesson')
        if lesson and lesson.is_full:
            raise serializers.ValidationError({"lesson": _("Это занятие уже заполнено.")})
        
        # Проверяем, что ребенок принадлежит текущему пользователю
        child = attrs.get('child')
        user = self.context['request'].user
        
        if child and child.parent != user:
            raise serializers.ValidationError({"child": _("Этот ребенок не принадлежит вам.")})
        
        if Enrollment.objects.filter(lesson=lesson, user=user, child=child).exists():
            raise serializers.ValidationError(_("Вы уже записаны на этот урок."))
        

        return attrs
    
    def create(self, validated_data):
        # Добавляем текущего пользователя в запись
        validated_data['user'] = self.context['request'].user
        
        # Создаем запись
        enrollment = Enrollment.objects.create(**validated_data)
        
        return enrollment


class CourseDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для курса с занятиями"""
    
    category = CourseCategorySerializer(read_only=True)
    lessons = SimpleLessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'name', 'slug', 'description', 'category',
            'age_group', 'format', 'price', 'duration', 'image',
            'is_active', 'lessons'
        ] 

class UserLessonSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name')
    available_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'name', 'description', 'teacher_name',
            'start_time', 'end_time', 'location', 'available_seats'
        ]

