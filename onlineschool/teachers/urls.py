from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='dashboard'),
    path('', views.teacher_list, name='teacher_list'),
    path('<int:pk>/', views.teacher_detail, name='teacher_detail'),
]