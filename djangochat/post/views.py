from django.shortcuts import render, redirect
from .forms import RegistrationForm, ReportForm
from .models import Registration

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some-view-name')  # Redirect to a success or home page
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('some-view-name')  # Redirect to a success or home page
    else:
        form = ReportForm()
    return render(request, 'report.html', {'form': form})
