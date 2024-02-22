# urls.py

from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    # Add more URL patterns as needed
]
