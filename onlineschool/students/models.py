from django.db import models
from django.conf import settings
from django.utils import timezone

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Tutor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class Session(models.Model):
    subject = models.CharField(max_length=100)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='sessions')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='booked_sessions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    start_time = models.DateTimeField()
    duration = models.IntegerField(default=60)
    mode = models.CharField(max_length=50, default='online')
    video_url = models.URLField(blank=True, null=True)
    
    SESSION_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('rescheduled', 'Rescheduled'),
    ]
    status = models.CharField(max_length=20, choices=SESSION_STATUS_CHOICES, default='scheduled')

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.subject} with {self.tutor.user.get_full_name()} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def is_upcoming(self):
        return self.start_time > timezone.now() and self.status == 'scheduled'

    def is_past(self):
        return self.start_time <= timezone.now() or self.status in ['completed', 'canceled']

    def get_absolute_url(self):
        return reverse("students:session_detail", kwargs={"pk": self.pk})

class Quiz(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    test_date = models.DateField()
    test_result = models.FloatField()

class Rating(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    score = models.IntegerField()

class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)

class SessionBooking(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='confirmed')

class Payment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    method = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
