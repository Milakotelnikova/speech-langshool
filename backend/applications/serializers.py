from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import Application
from courses.models import CourseCategory
from courses.serializers import CourseCategorySerializer


class ApplicationSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и просмотра заявок"""
    
    course = CourseCategorySerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=CourseCategory.objects.all(), 
        source='course',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Application
        fields = [
            'id', 'name', 'phone', 'email', 'child_name',
            'child_age', 'course', 'course_id', 'status',
            'created_at', 'study_type'
        ]
        read_only_fields = ['status', 'created_at', 'admin_notes']
    def validate_phone(self, value):
        """Базовая валидация телефона"""
        # Удаление всех нецифровых символов из номера
        phone = ''.join(filter(str.isdigit, value))
        if len(phone) < 10:
            print('validator')
            raise serializers.ValidationError(_("Номер телефона должен содержать минимум 10 цифр."))
            
        return value




class AdminApplicationSerializer(ApplicationSerializer):
    """Расширенный сериализатор для администраторов с дополнительными полями"""
    
    class Meta(ApplicationSerializer.Meta):
        fields = ApplicationSerializer.Meta.fields + ['admin_notes']
        read_only_fields = ['created_at'] 