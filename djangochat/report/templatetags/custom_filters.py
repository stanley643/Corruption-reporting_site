# app_name/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='file_type')
def file_type(value):
    if value.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return 'image'
    elif value.endswith(('.mp4', '.avi', '.mov')):
        return 'video'
    elif value.endswith(('.mp3', '.wav', '.ogg')):
        return 'audio'
    elif value.endswith(('.docx', '.pdf', '.txt', '.doc')):
        return 'document'
    else:
        return 'other'
