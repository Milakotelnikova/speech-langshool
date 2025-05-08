from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Teacher, CourseCategory, Course, Lesson, Enrollment


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'email', 'phone')


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'format', 'age_group', 'is_active')
    list_filter = ('category', 'format', 'age_group', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ('category',)


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    raw_id_fields = ('user', 'child')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'teacher', 'start_time', 'end_time', 'location', 'max_students', 'get_available_seats')
    list_filter = ('course', 'teacher', 'start_time')
    search_fields = ('name', 'description', 'location')
    autocomplete_fields = ('course', 'teacher')
    inlines = [EnrollmentInline]
    
    def get_available_seats(self, obj):
        return obj.available_seats
    
    get_available_seats.short_description = _('Available seats')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'child', 'lesson', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'lesson')
    search_fields = ('user__email', 'user__name', 
                   'child__name', 'lesson__name')
    autocomplete_fields = ('user', 'child', 'lesson')
