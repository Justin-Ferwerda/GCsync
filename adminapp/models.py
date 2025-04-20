from django.contrib.auth.models import User
from django.db import models

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    google_id = models.CharField(max_length=100, unique=True)
    access_token = models.TextField()
    refresh_token = models.TextField()

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class ClassroomAssignment(models.Model):
    title = models.CharField(max_length=255)
    course_id = models.CharField(max_length=50)
    coursework_id = models.CharField(max_length=50)
    due_date = models.DateField(null=True, blank=True)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    teachers = models.ManyToManyField(Teacher, related_name="assignments")

    def __str__(self):
        return self.title
