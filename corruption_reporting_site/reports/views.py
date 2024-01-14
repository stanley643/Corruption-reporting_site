from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
# Create your views here.
from rest_framework import generics
from .models import Report
from .serializers import ReportSerializer

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
    