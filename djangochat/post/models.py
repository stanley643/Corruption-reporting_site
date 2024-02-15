from django.db import models
from django.contrib.auth.hashers import make_password

class Registration(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Length to accommodate hashed password

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Registration, self).save(*args, **kwargs)

