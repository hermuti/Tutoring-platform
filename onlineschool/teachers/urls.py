from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.tutor_dashboard, name='tutor_dashboard'),
]