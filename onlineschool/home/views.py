from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomLoginForm, CustomRegisterForm
from .models import CustomUser
from django.contrib import messages

def home_view(request):
    return render(request, 'home/home.html')

class CustomLoginView(LoginView):
    template_name = 'home/login.html'
    authentication_form = CustomLoginForm

    def form_valid(self, form):
        role = self.request.POST.get('role')
        user = form.get_user()
        if role != user.role:
            form.add_error(None, "Role mismatch.")
            return self.form_invalid(form)

        login(self.request, user)
        if role == 'student':
            return redirect('students:dashboard')  # Change based on your URLs
        elif role == 'teacher':
            return redirect('teachers:dashboard')
        else:
            return redirect('/admin/')

def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('home:login')
    else:
        form = CustomRegisterForm()
    return render(request, 'home/register.html', {'form': form})
