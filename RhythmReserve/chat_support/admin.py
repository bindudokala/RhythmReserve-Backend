from django.contrib import admin
from .models import ChatSession, Message

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'session_start']
    list_filter = ['session_start']
    search_fields = ['user_name']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'text', 'created_at', 'sender']
    list_filter = ['created_at', 'sender']
    search_fields = ['text', 'session__user_name']
    raw_id_fields = ['session']  # Helps in handling admin with a large number of sessions
