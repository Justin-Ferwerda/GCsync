from django.contrib.auth.models import AbstractUser
from django.db import models

class Teacher(AbstractUser):
    
    is_synced = models.BooleanField(default=False)
