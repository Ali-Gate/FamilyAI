# api/admin.py
from django.contrib import admin
from .models import AIInteraction, AIConversationSession

@admin.register(AIConversationSession)
class AIConversationSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'started_at', 'ended_at')
    list_filter = ('ended_at',)

@admin.register(AIInteraction)
class AIInteractionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session', 'created_at')
    list_filter = ('session', 'created_at')
