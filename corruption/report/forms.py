from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserAuthentication, Post

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = UserAuthentication
        fields = ['email', 'username', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'item_type', 'file', 'description']