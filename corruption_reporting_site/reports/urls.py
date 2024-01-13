from django.urls import path
from .views import ReportListCreate

urlpatterns = [
    path('api/reports/', ReportListCreate.as_view(), name='report-list-create'),
]
