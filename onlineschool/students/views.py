from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin # To restrict access to logged-in users [24]
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.utils import timezone

from .models import Session, StudentProfile, Tutor

# 1. Student Dashboard View (matches student.jpg)
class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "students/student_dashboard.html"
    login_url = reverse_lazy('login') # Redirects to this URL if user is not logged in [25]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current logged-in user's student profile
        try:
            student_profile = self.request.user.studentprofile
        except StudentProfile.DoesNotExist:
            # Handle case where a User might not have a StudentProfile (e.g., an admin logging in)
            student_profile = None 

        if student_profile:
            # Fetch upcoming sessions for this student, ordered by time
            upcoming_sessions = Session.objects.filter(
                student=student_profile,
                start_time__gt=timezone.now(),
                status='scheduled'
            ).order_by('start_time')

            context['upcoming_sessions'] = upcoming_sessions
            context['student_profile'] = student_profile # Pass the student profile to the template
        else:
            context['upcoming_sessions'] = [] # No sessions if no student profile
            context['student_profile'] = None
        
        # You can add other context variables here, e.g., session history, progress data
        # context['session_history'] = Session.objects.filter(
        #     student=student_profile,
        #     status__in=['completed', 'canceled', 'rescheduled']
        # ).order_by('-start_time') # Order by most recent first

        return context

# 2. Session Detail View (for "View Details" button)
class SessionDetailView(LoginRequiredMixin, DetailView):
    model = Session # The model this view will operate on [26]
    template_name = "students/session_detail.html" # The template to render [27]
    context_object_name = "session" # The variable name in the template context [28, 29]

    def get_queryset(self):
        # Ensure only the logged-in student can view details of their own sessions
        try:
            student_profile = self.request.user.studentprofile
            return Session.objects.filter(student=student_profile)
        except StudentProfile.DoesNotExist:
            return Session.objects.none() # Return an empty queryset if no profile

# 3. Session Action View (for "Join Session", "Reschedule", "Cancel" buttons)
# This view handles POST requests to change the status of a session.
class SessionActionView(LoginRequiredMixin, View):
    def post(self, request, pk, action, *args, **kwargs):
        session = get_object_or_404(Session, pk=pk) # Get the session object [30]
        
        # Security check: Ensure the session belongs to the logged-in student
        try:
            if session.student != request.user.studentprofile:
                return HttpResponseForbidden("You do not have permission to perform this action on this session.")
        except StudentProfile.DoesNotExist:
            return HttpResponseForbidden("Student profile not found.")

        if action == 'cancel':
            # Logic to cancel the session
            if session.is_upcoming(): # Only allow cancelling upcoming sessions
                session.status = 'canceled'
                session.save()
                # You might add Django messages here for user feedback
                # from django.contrib import messages
                # messages.success(request, f"Session '{session.subject}' has been cancelled.")
            else:
                # messages.error(request, "Only upcoming sessions can be cancelled.")
                pass # Or return an appropriate error response
        
        elif action == 'join':
            # Logic to "join" the session (e.g., redirect to a video conference URL)
            if session.is_upcoming():
                # For demo, just update status. In real app, redirect to a meeting URL
                # session.status = 'in_progress' # Or whatever status fits
                # session.save()
                # return redirect(session.meeting_url) # If you have a URL in your model
                return HttpResponse("Redirecting to meeting for session: %s" % session.subject)
            else:
                return HttpResponse("Cannot join this session as it's not upcoming.")
        
        elif action == 'reschedule':
            # Logic for rescheduling. This typically involves redirecting to a form
            # where the user can pick a new date/time.
            # You would create a separate RescheduleSessionForm and corresponding view.
            return HttpResponse("Redirect to reschedule form for session %s" % session.subject)
        
        # Always redirect after a successful POST to prevent double submission [31]
        return HttpResponseRedirect(reverse('students:student_dashboard'))
