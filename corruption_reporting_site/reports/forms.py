# forms.py
from django import forms
from django.contrib.auth import get_user_model

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['phone_number']

class VerificationForm(forms.Form):
    code = forms.CharField(max_length=10)
