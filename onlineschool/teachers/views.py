from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SessionSerializer
from students.models import Session, Tutor
from django.utils import timezone

from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Session, Tutor
from django.utils import timezone
from django.contrib.auth.models import User

@login_required
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
