from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from .models import TeacherProfile # Create TeacherProfile model
from .models import Teacher

@login_required
def teacher_dashboard(request):
    # teacher = TeacherProfile.objects.get(user=request.user) # Uncomment when TeacherProfile exists
    return render(request, 'teachers/dashboard.html', {'teacher': request.user})

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

def teacher_detail(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})
