from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Teacher

@receiver(post_save, sender=Teacher)
def teacher_verification_notification(sender, instance, **kwargs):
    if instance.is_verified:
        subject = 'Your Teacher Account Has Been Verified'
        message = f'Dear {instance.user.first_name},\n\nYour teacher account has been verified. You can now access all the features of the platform.'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [instance.user.email]

        send_mail(subject, message, from_email, to_email, fail_silently=False)