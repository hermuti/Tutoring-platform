from django.db import models
from django.conf import settings
from django.utils import timezone # For handling dates and times for sessions

# StudentProfile model to extend Django's User model [16, 17]
class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    # Add any student-specific fields here that are not in the default User model
    # student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    # profile_picture = models.ImageField(upload_to='student_profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

# Tutor (Professor) model
class Tutor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    # Add tutor-specific fields here (e.g., expertise, bio)
    # expertise = models.CharField(max_length=100)
    # bio = models.TextField(blank=True)

    def __str__(self):
        # Display the tutor's full name, or username if not set
        return self.user.get_full_name() or self.user.username

# Session model
class Session(models.Model):
    subject = models.CharField(max_length=100) # e.g., "Mathematics - Algebra", "Physics - Mechanics"
    
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='sessions') # Professor name from DB [18]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='booked_sessions')
    
    start_time = models.DateTimeField() # Date and time of the session
    
    # Status of the session, for filtering upcoming/past sessions and actions
    SESSION_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('rescheduled', 'Rescheduled'),
    ]
    status = models.CharField(max_length=20, choices=SESSION_STATUS_CHOICES, default='scheduled')

    class Meta:
        ordering = ['start_time'] # Order sessions by their start time [19]

    def __str__(self):
        return f"{self.subject} with {self.tutor.user.get_full_name()} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def is_upcoming(self):
        """Checks if the session is in the future and scheduled."""
        return self.start_time > timezone.now() and self.status == 'scheduled'

    def is_past(self):
        """Checks if the session has already occurred or is completed/canceled."""
        return self.start_time <= timezone.now() or self.status in ['completed', 'canceled']

    # Method to get the absolute URL for a session's detail page
    from django.urls import reverse
    def get_absolute_url(self):
        return reverse("students:session_detail", kwargs={"pk": self.pk})
