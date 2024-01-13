from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Report
from .serializers import ReportSerializer

class ReportListCreate(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
