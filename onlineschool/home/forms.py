# home/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class CustomLoginForm(AuthenticationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        role = self.cleaned_data.get('role')

        super().clean()
        user = self.get_user()

        if user and role != user.role:
            raise forms.ValidationError("Role mismatch.")

        return self.cleaned_data

class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']