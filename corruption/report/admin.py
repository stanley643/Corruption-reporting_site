from django.contrib import admin
from .models import UserAuthentication, Post
# Register your models here.

admin.site.register(UserAuthentication)
admin.site.register(Post)