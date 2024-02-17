from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('report/', views.create_report, name='create_report')

]