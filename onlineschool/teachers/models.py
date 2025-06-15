from django.db import models
from django.conf import settings

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name() or self.user.username