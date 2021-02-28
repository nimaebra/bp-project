from django.db import models

from teacher.models import Practice


class Answer(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    file = models.FileField(upload_to='answers/')
    score = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.practice)
