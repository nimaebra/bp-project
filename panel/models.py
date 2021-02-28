from django.db import models


class Practice(models.Model):
    title = models.CharField(max_length=200)
    comment = models.CharField(max_length=500)
    deadline = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
