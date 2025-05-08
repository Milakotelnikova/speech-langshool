from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User, Child


class ChildSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ребенка"""
    
    class Meta:
        model = Child
        fields = ['id', 'name', 'age', 'created_at']
        read_only_fields = ['created_at']


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""
    
    children = ChildSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 
                  'is_parent', 'date_joined', 'children']
        read_only_fields = ['date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя"""
    email = serializers.EmailField(
        required=True,
        validators=[]  #  -UniqueValidator чтобы выводить кастомные ошибки
    )

    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'is_parent', 'password', 'password_confirm']
        extra_kwargs = {
            'name': {'required': True},
        }

    # Проверка почты
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с такиой почтой уже зарегистрирован.")
        return value


    def validate(self, attrs):
        # Проверяем совпадение паролей
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": _("Пароли не совпадают.")})
                
        # Проверяем надежность пароля
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
            
        return attrs
    
    def create(self, validated_data):
        # Удаляем поле подтверждения пароля
        validated_data.pop('password_confirm')
        
        # Создаем пользователя
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            phone=validated_data.get('phone', ''),
            is_parent=validated_data.get('is_parent', False),
        )
        
        return user


class LoginSerializer(serializers.Serializer):
    """Сериализатор для авторизации пользователя"""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, required=True, write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            
            if not user:
                msg = _('Неверная почта или пароль.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Необходимо указать почту и пароль.')
            raise serializers.ValidationError(msg, code='authorization')
            
        attrs['user'] = user
        return attrs

class ChildCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания записи о ребенке"""
    
    class Meta:
        model = Child
        fields = ['name', 'age']
        
    def create(self, validated_data):
        # Получаем текущего пользователя
        user = self.context['request'].user
        
        # Создаем запись о ребенке
        child = Child.objects.create(
            parent=user,
            **validated_data
        )
        
        return child


class PasswordChangeSerializer(serializers.Serializer):
    """Сериализатор для смены пароля"""
    
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password_confirm = serializers.CharField(required=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        # Проверяем совпадение новых паролей
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": _("Пароли не совпадают.")})
        
        # Проверяем надежность нового пароля
        try:
            validate_password(attrs['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
            
        return attrs
    
    def validate_old_password(self, value):
        # Проверяем старый пароль
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Неверный текущий пароль."))
        return value 