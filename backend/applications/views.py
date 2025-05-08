from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import Application
from .serializers import ApplicationSerializer, AdminApplicationSerializer


class ApplicationCreateView(generics.CreateAPIView):
    """View для создания заявки на урок"""
    
    serializer_class = ApplicationSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        # Сохраняем заявку
        application = serializer.save()
        
        # Отправляем уведомление администратору
        self.send_admin_notification(application)
        
    def send_admin_notification(self, application):
        """Отправка уведомления администратору о новой заявке"""

        subject = 'Новая заявка на пробное занятие'

        # Проверка на null для каждого поля
        message = f'''
        Поступила новая заявка:

        Имя: {application.name}
        Email: {application.email}
        Телефон: {application.phone}
        Возраст ребенка: {application.child_age if application.child_age else 'Не указан'}
        Имя ребенка: {application.child_name if application.child_name else 'Не указано'}
        Курс: {application.course.name if application.course else 'Не указан'}
        '''

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.ADMIN_EMAIL]

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False
        )



# Административные view для управления заявками
class AdminApplicationListView(generics.ListAPIView):
    """View для просмотра списка заявок (только для администраторов)"""
    
    serializer_class = AdminApplicationSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        queryset = Application.objects.all()
        
        # Фильтр по статусу
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset.order_by('-created_at')


class AdminApplicationDetailView(generics.RetrieveUpdateAPIView):
    """View для просмотра и обновления заявки (только для администраторов)"""
    
    queryset = Application.objects.all()
    serializer_class = AdminApplicationSerializer
    permission_classes = [IsAdminUser]
