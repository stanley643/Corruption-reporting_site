from django.contrib import admin
from .models import Report, UserProfile, ChatMessage, customuser


admin.site.register(Report)
admin.site.register(UserProfile)
admin.site.register(ChatMessage)
admin.site.register(customuser)