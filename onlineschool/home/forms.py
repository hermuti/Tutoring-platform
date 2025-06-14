# home/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class CustomLoginForm(AuthenticationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']