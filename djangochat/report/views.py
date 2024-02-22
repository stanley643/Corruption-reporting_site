# views.py

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy

# View for displaying a list of posts
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'  # Replace with your template name
    context_object_name = 'posts'

# View for displaying details of a post
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'  # Replace with your template name
    context_object_name = 'post'

# View for creating a new post
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm  # Replace with your form class if you have one
    template_name = 'post_form.html'  # Replace with your template name

    def form_valid(self, form):
        # Perform additional actions if needed before saving the form
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post-list')