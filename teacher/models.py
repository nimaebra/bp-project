from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


# class Role(models.Model):
#     '''
#     The Role entries are managed by the system,
#     automatically created via a Django data migration.
#     '''
#     STUDENT = 1
#     TEACHER = 2
#     ADMIN = 3
#     ROLE_CHOICES = (
#         (STUDENT, 'student'),
#         (TEACHER, 'teacher'),
#         (ADMIN, 'admin'),
#     )

#     id = models.PositiveSmallIntegerField(
#         choices=ROLE_CHOICES, primary_key=True)

#     def __str__(self):
#         return self.get_id_display()

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# class User(AbstractUser):
#     roles = models.ManyToManyField(Role)


class Practice(models.Model):
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    comment = models.CharField(max_length=500)
    deadline = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Video(models.Model):
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
