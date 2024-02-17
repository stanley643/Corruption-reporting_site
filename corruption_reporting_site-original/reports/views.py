from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
# Create your views here.
from rest_framework import generics
from .models import CustomUser, Report
from .serializers import ReportSerializer
import random

class ReportListCreate(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
class ReportListView(ListView):
    model = Report
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/report_detail.html'

class ReportCreateView(CreateView):
    model = Report
    template_name = 'reports/report_form.html'
    fields = ['title', 'description', 'evidence_file']

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)
    success_url = reverse_lazy('report-list')  # Redirect to the report list page after creation


def chat_room(request, room_name):
    return render(request, 'reports/chat_room.html', {
        'room_name': room_name
    })

def register(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        # Generate a random verification code
        verification_code = f"KE-{random.randint(1000, 9999)}"
        # Send the verification code to the phone number
        # (You'll need to integrate an SMS service for this)

        # Store the phone number and verification code in the session
        request.session['phone_number'] = phone_number
        request.session['verification_code'] = verification_code

        # Redirect to verification page
        return redirect('verify_code')

    return render(request, 'register.html')


def verify_code(request):
    if request.method == 'POST':
        user_code = request.POST.get('code')
        if user_code == request.session.get('verification_code'):
            # Create the user account
            CustomUser.objects.create_user(
                phone_number=request.session['phone_number']
            )
            # Redirect to the login page or directly log the user in
            return redirect('login')
        else:
            # Handle incorrect verification code
            pass

    return render(request, 'verify_code.html')

