from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'child_age', 'course', 'status', 'created_at', 'study_type')
    list_filter = ('status', 'created_at', 'course')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)
    raw_id_fields = ('course',)
    fieldsets = (
        (_('Contact Information'), {
            'fields': ('name', 'email', 'phone', 'child_age')
        }),
        (_('Course Information'), {
            'fields': ('course',)
        }),
        (_('Status'), {
            'fields': ('status', 'created_at', 'admin_notes')
        }),
    )
