# api/serializers.py
from rest_framework import serializers
from .models import AIInteraction, AIConversationSession
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class AIConversationSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = AIConversationSession
        fields = ['id', 'user', 'started_at', 'ended_at']
        read_only_fields = ['started_at', 'ended_at']

class AIInteractionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    session = AIConversationSessionSerializer(read_only=True)
    
    class Meta:
        model = AIInteraction
        fields = ['id', 'user', 'session', 'input', 'response', 'created_at', 'responded_at']
        read_only_fields = ['response', 'created_at', 'responded_at']