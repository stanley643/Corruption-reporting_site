from django.urls import path
from .views import register, post_detail, post_list, view_media, serve_media

urlpatterns = [
    path('register/', register, name='register'),
    path('list/', post_list, name='post_list'),  # URL for the post list view
    path('post/<int:pk>/', post_detail, name='post_detail'),  # URL for the post detail view
    path('view/', view_media, name='view_media'),
    path('serve/<int:post_id>/', serve_media, name='serve_media'),
]
