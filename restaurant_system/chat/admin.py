from django.contrib import admin
from .models import ChatThread, ChatMessage

@admin.register(ChatThread)
class ChatThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "is_open", "created_at")
    list_filter = ("is_open",)
    search_fields = ("customer__username",)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("thread", "sender", "created_at")
    search_fields = ("content", "sender__username")
    list_filter = ("created_at",)
