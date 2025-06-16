from django.contrib.auth.views import LoginView
from teachers.models import Teacher
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

        if not user.is_active:
            form.add_error(None, "This account is inactive.")
            return self.form_invalid(form)

        print(f"Form role: {role}")
        print(f"User role: {user.role}")
        print(f"Form is valid: {form.is_valid()}")

        login(self.request, user)
        if role == 'student':
            return redirect('students:student_dashboard')
        elif role == 'teacher':
            try:
                teacher = Teacher.objects.get(user=user)
                if not teacher.is_verified:
                    # Check if the teacher profile is complete
                    if not teacher.bio or not teacher.qualifications or not teacher.documents.name:
                        return redirect('teachers:teacher_profile_completion')
                    else:
                        return redirect('teachers:pending_verification')
                return redirect('teachers:tutor_dashboard')
            except Teacher.DoesNotExist:
                form.add_error(None, "Teacher profile not found. Please contact the administrator.")
                return self.form_invalid(form)
        else:
            return redirect('/admin/')

def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.role == 'teacher':
                teacher = Teacher.objects.create(user=user)
                messages.success(request, "Account created successfully. Please complete your profile.")
                return redirect('teachers:teacher_profile_completion')
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('home:login')
    else:
        form = CustomRegisterForm()
    return render(request, 'home/register.html', {'form': form})
