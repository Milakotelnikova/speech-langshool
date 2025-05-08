import uuid

from django.shortcuts import render
from django.contrib.auth import login, logout
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_GET



from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

from .models import User, Child
from .serializers import (
    UserSerializer, UserRegistrationSerializer, LoginSerializer,
    ChildSerializer, ChildCreateSerializer, PasswordChangeSerializer
)

# def get_csrf_token(request):
#     return JsonResponse({'csrfToken': get_token(request)})



@api_view(['GET'])
@permission_classes([AllowAny])
def csrf(request):
    token = get_token(request)
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = token
    return response


class UserRegistrationView(generics.CreateAPIView):
    """View для регистрации нового пользователя"""
    
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Логиним пользователя после регистрации
            login(request, user)
            
            # Формируем ответ
            return Response(
                {"detail": _("Регистрация успешна."), "user": UserSerializer(user).data},
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """View для входа пользователя"""
    
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            
            return Response(
                {"detail": _("Вход выполнен успешно."), "user": UserSerializer(user).data},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """View для выхода пользователя"""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"detail": _("Выход выполнен успешно.")}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View для просмотра и обновления профиля пользователя"""
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChildListView(generics.ListAPIView):
    """View для получения списка детей пользователя"""
    
    serializer_class = ChildSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Child.objects.filter(parent=self.request.user)


class ChildCreateView(generics.CreateAPIView):
    """View для добавления ребенка"""
    
    serializer_class = ChildCreateSerializer
    permission_classes = [IsAuthenticated]


class ChildDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View для просмотра, обновления и удаления информации о ребенке"""
    
    serializer_class = ChildSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Пользователь может работать только со своими детьми
        return Child.objects.filter(parent=self.request.user)


