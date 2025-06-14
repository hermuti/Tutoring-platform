from django.urls import path
from .views import CustomLoginView, register_view, home_view

app_name = 'home'

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),
]