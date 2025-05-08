from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User, Child


class Teacher(models.Model):
    """Модель преподавателя языковой школы"""
    
    name = models.CharField(_('first name'), max_length=150)
    bio = models.TextField(_('biography'), blank=True)
    photo = models.ImageField(_('photo'), upload_to='teachers/', blank=True, null=True)
    
    email = models.EmailField(_('email'), blank=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('преподаватель')
        verbose_name_plural = _('преподаватели')
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name}"


class CourseCategory(models.Model):
    """Категория курса (например, испанский язык, английский для детей и т.д.)"""
    
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('категория курса')
        verbose_name_plural = _('категории курсов')
        ordering = ['name']
        
    def __str__(self):
        return self.name


class Course(models.Model):
    """Модель курса в языковой школе"""
    
    AGE_CHOICES = (
        ('kids', _('Для детей')),
        ('adults', _('Для взрослых')),
        ('all', _('Для всех возрастов')),

    )
    
    FORMAT_CHOICES = (
        ('online', _('Онлайн')),
        ('offline', _('Офлайн')),
        ('hybrid', _('Смешанный формат')),

    )
    
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'))
    
    category = models.ForeignKey(
        CourseCategory, 
        on_delete=models.CASCADE, 
        related_name='courses',
        verbose_name=_('category')
    )
    
    age_group = models.CharField(_('age group'), max_length=10, choices=AGE_CHOICES, default='all')
    format = models.CharField(_('format'), max_length=10, choices=FORMAT_CHOICES, default='offline')
    
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(_('duration in hours'), help_text=_('Общая продолжительность курса в часах'))
    
    image = models.ImageField(_('image'), upload_to='courses/', blank=True, null=True)
    
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('курс')
        verbose_name_plural = _('курсы')
        ordering = ['name']
        
    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Модель занятия по курсу"""
    
    name = models.CharField(_('name'), max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lessons')
    
    description = models.TextField(_('description'), blank=True)
    
    start_time = models.DateTimeField(_('start time'))
    end_time = models.DateTimeField(_('end time'))
    
    location = models.CharField(_('location'), max_length=250, blank=True,
                              help_text=_('Адрес или онлайн-ссылка'))
    
    max_students = models.PositiveIntegerField(_('maximum students'), default=10)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('занятие')
        verbose_name_plural = _('занятия')
        ordering = ['start_time']
        
    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%d.%m.%Y %H:%M')})"
    
    @property
    def is_full(self):
        """Проверяет, заполнено ли занятие до максимума"""
        return self.enrollments.count() >= self.max_students
    
    @property
    def available_seats(self):
        """Возвращает количество свободных мест"""
        return max(0, self.max_students - self.enrollments.count())


class Enrollment(models.Model):
    """Модель записи на занятие"""
    
    STATUS_CHOICES = (
        ('confirmed', _('Подтверждено')),
        ('cancelled', _('Отменено')),
        ('pending', _('Ожидает подтверждения')),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    child = models.ForeignKey(Child, on_delete=models.SET_NULL, null=True, blank=True, 
                             related_name='enrollments')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='enrollments')
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('запись на занятие')
        verbose_name_plural = _('записи на занятия')
        ordering = ['-created_at']
        # Пользователь может записать только одного ребенка на одно занятие
        unique_together = [['lesson', 'child']]
        
    def __str__(self):
        student_name = self.child.name if self.child else self.user.name
        return f"{student_name} - {self.lesson.name} ({self.get_status_display()})"
