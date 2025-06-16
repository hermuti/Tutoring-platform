from django.db import models
from django.conf import settings

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    is_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    qualifications = models.TextField(blank=True)
    documents = models.FileField(upload_to='teachers/documents/', blank=True)
    years_of_experience = models.IntegerField(default=0)
    STATUS_CHOICES = [
        ('pending_review', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending_review'
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username