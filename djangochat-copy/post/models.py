from django.db import models
from django.contrib.auth.hashers import make_password
#from django.conf import settings

class Registration(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Length to accommodate hashed password

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Registration, self).save(*args, **kwargs)

class Report(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reporter = models.ForeignKey(Registration, on_delete=models.CASCADE)
    evidence_file = models.FileField(upload_to='evidences/')
