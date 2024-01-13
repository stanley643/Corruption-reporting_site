from django.contrib import admin
from .models import Report, UserProfile, ChatMessage


admin.site.register(Report)
admin.site.register(UserProfile)
admin.site.register(ChatMessage)
