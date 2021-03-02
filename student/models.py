from django.db import models
from django.contrib.auth.models import User

from teacher.models import Practice


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    student_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Answer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE, default=1)
    file = models.FileField(upload_to='answers/')
    score = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.practice)
