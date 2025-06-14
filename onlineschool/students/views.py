from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Student # Assuming Student model exists
# from .models import StudentProfile # Create StudentProfile model
from .models import Student
@login_required
def student_dashboard(request):
    # student = StudentProfile.objects.get(user=request.user) # Uncomment when StudentProfile exists
    student = Student.objects.get(id=request.user.id)
    return render(request, 'students/dashboard.html', {'student': student})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

def student_detail(request, pk):
    student = Student.objects.get(pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})
