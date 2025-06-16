from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SessionSerializer
from students.models import Session, Tutor
from django.utils import timezone

from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from students.models import Session, Tutor
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import TeacherProfileForm
from .decorators import teacher_required
from .models import Teacher

@login_required
@teacher_required
def tutor_dashboard(request):
    try:
        tutor = Tutor.objects.get(user=request.user)
    except Tutor.DoesNotExist:
        return render(request, 'teachers/tutor_dashboard.html', {'error': 'Tutor profile not found.'})

    upcoming_sessions = Session.objects.filter(
        tutor=tutor,
        start_time__gt=timezone.now(),
        status='scheduled'
    ).order_by('start_time')

    context = {
        "tutor_name": request.user.first_name,
        "sessions": upcoming_sessions,
    }
    return render(request, 'teachers/tutor_dashboard.html', context)

@login_required
def teacher_profile_completion(request):
    try:
        teacher, created = Teacher.objects.get_or_create(user=request.user)
    except Teacher.DoesNotExist:
        teacher = Teacher.objects.create(user=request.user)

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teachers:pending_verification')  # Redirect to pending verification page
    else:
        form = TeacherProfileForm(instance=teacher)

    return render(request, 'teachers/teacher_profile_completion.html', {'form': form})

@login_required
def pending_verification(request):
    return render(request, 'teachers/pending_verification.html')
