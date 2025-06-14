from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('', views.student_list, name='student_list'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
]