from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    evidence_file = models.FileField(upload_to='evidences/')
