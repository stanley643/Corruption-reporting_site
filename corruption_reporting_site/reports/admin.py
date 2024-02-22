from django.contrib import admin
from .models import Report, UserProfile, Message, CustomUser


admin.site.register(Report)
admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(CustomUser)