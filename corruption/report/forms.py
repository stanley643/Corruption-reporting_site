from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserAuthentication

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = UserAuthentication
        fields = ['email', 'username', 'password1', 'password2']
