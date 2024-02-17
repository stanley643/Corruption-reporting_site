from django import forms
from .models import Registration, Report

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['username', 'email', 'password']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'reporter', 'evidence_file']