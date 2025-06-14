from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import StudentProfile, Tutor # Import your new models

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    # This signal receiver will be called every time a User object is saved.
    # 'created' is True if the user was just created, False if updated.
    if created:
        # For simplicity, assuming new users are students. In a real app,
        # your registration process would determine if they are a student or tutor.
        StudentProfile.objects.create(user=instance)
        # If you need to create a Tutor profile instead/additionally:
        # Tutor.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.studentprofile.save()
    except StudentProfile.DoesNotExist:
        # Handle cases where a User might not have a StudentProfile (e.g., it's a Tutor or admin)
        pass