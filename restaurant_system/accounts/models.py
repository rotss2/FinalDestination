from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=32, blank=True)
    is_support = models.BooleanField(default=False, help_text="Can handle live chat support.")

    def __str__(self):
        return self.get_username()
