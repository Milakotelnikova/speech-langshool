from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # Публичные маршруты
    path('apply/', views.ApplicationCreateView.as_view(), name='application-create'),
    
    # Административные маршруты
    path('admin/applications/', views.AdminApplicationListView.as_view(), name='admin-application-list'),
    path('admin/applications/<int:pk>/', views.AdminApplicationDetailView.as_view(), name='admin-application-detail'),
] 