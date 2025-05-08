from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Менеджер пользователей с кастомной логикой создания"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Создает и сохраняет пользователя с указанным email и паролем"""
        if not email:
            raise ValueError(_('Email должен быть указан'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и сохраняет суперпользователя с указанным email и паролем"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True'))
            
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя"""
    
    username = None
    last_name = None
    first_name = None
    email = models.EmailField(_('email address'), unique=True)
    
    name = models.CharField(_('first_name'), max_length=150)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    
    # Для родителей, которые регистрируют детей
    is_parent = models.BooleanField(_('is parent'), default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи') 
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} <{self.email}>"


class Child(models.Model):
    """Модель ребенка, связанная с родителем"""
    
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(_('first name'), max_length=150)
    age = models.PositiveSmallIntegerField(_('age'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('ребенок')
        verbose_name_plural = _('дети')
        ordering = ['parent', 'name']
        
    def __str__(self):
        return f"{self.name} ({self.age})"

