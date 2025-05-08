from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # CSRF токен
    path('csrf/', views.csrf, name='csrf'),


    # Аутентификация
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Работа с профилем
    path('profile/', views.UserProfileView.as_view(), name='profile'),
        
    # Управление детьми
    path('children/', views.ChildListView.as_view(), name='child-list'),
    path('children/add/', views.ChildCreateView.as_view(), name='child-create'),
    path('children/<int:pk>/', views.ChildDetailView.as_view(), name='child-detail'),
] 