from django.urls import path
from . import views
from .decorators import teacher_required

urlpatterns = [
    path('dashboard/', teacher_required(views.tutor_dashboard), name='tutor_dashboard'),
    path('profile/complete/', views.teacher_profile_completion, name='teacher_profile_completion'),
    path('pending/verification/', views.pending_verification, name='pending_verification'),
]