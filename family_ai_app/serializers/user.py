from rest_framework import serializers
from django.contrib.auth.models import User
from family_ai_app.models import Message

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    tickets_count = serializers.IntegerField(source='tickets.count', read_only=True)
    messages_count = serializers.SerializerMethodField()
    notifications_unseen = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'tickets_count',
            'messages_count',
            'notifications_unseen',
        ]
        read_only_fields = [
            'id',
            'tickets_count',
            'messages_count',
            'notifications_unseen',
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_messages_count(self, obj):
        return Message.objects.filter(sender=obj).count()

    def get_notifications_unseen(self, obj):
        return obj.notifications.filter(is_seen=False).count()
