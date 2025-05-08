from django.db import models
from django.utils.translation import gettext_lazy as _
from courses.models import CourseCategory


class Application(models.Model):
    """Модель заявки от потенциального клиента"""
    
    STATUS_CHOICES = (
        ('new', _('Новая')),
        ('processing', _('В обработке')),
        ('contacted', _('Связались')),
        ('converted', _('Конвертирована в клиента')),
        ('rejected', _('Отклонена')),
    )
    
    STUDY_TYPE_CHOICES = [
        ('school', 'Занятия в клубе'),
        ('online', 'Онлайн-занятия'),
    ]
    
    # Основная информация
    name = models.CharField(_('name'), max_length=100)
    phone = models.CharField(_('phone'), max_length=20)
    email = models.EmailField(_('email'))
    
    # Информация о ребенке
    child_name = models.CharField(_('child name'), blank=True, null=True)
    child_age = models.PositiveSmallIntegerField(_('child age'), blank=True, null=True)
    
    
    # Курс, которым интересуется
    course = models.ForeignKey(
        CourseCategory, 
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_('course')
    )

    # Тип обучения
    study_type = models.CharField(
        max_length=10,
        choices=STUDY_TYPE_CHOICES,
        default='school',
        verbose_name='Тип занятий'
    )

    # Статус и даты
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Административные заметки
    admin_notes = models.TextField(_('admin notes'), blank=True)
    
    class Meta:
        verbose_name = _('заявка')
        verbose_name_plural = _('заявки')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} - {self.email} ({self.get_status_display()})"

