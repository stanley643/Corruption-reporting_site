from django.urls import path
from .views import register, post_detail, post_list, view_media, serve_media, login_view, create_post, landing_page, logout_view

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('create_post/', create_post, name='create_post'),
    path('list/', post_list, name='post_list'),  # URL for the post list view
    path('post/<int:pk>/', post_detail, name='post_detail'),  # URL for the post detail view
    path('view/', view_media, name='view_media'),
    path('serve/<int:post_id>/', serve_media, name='serve_media'),
    path('logout/', logout_view, name='logout'),
]
