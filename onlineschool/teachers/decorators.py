from django.shortcuts import redirect
from functools import wraps
from .models import Teacher

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            teacher = Teacher.objects.get(user=request.user)
            if not teacher.is_verified:
                return redirect('teachers:pending_verification')
        except Teacher.DoesNotExist:
            return redirect('home')  # Or wherever non-teachers should go
        return view_func(request, *args, **kwargs)
    return _wrapped_view