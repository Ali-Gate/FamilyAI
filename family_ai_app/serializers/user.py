from rest_framework import serializers
from django.contrib.auth.models import User
from family_ai_app.models import Message
from .ticket import TicketSerializer  # import TicketSerializer

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    tickets_count = serializers.IntegerField(source='tickets.count', read_only=True)
    messages_count = serializers.SerializerMethodField()
    notifications_unseen = serializers.SerializerMethodField()
    recent_tickets = serializers.SerializerMethodField()

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
            'recent_tickets',
        ]
        read_only_fields = [
            'id',
            'tickets_count',
            'messages_count',
            'notifications_unseen',
            'recent_tickets',
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_messages_count(self, obj):
        return Message.objects.filter(sender=obj).count()

    def get_notifications_unseen(self, obj):
        return obj.notifications.filter(is_seen=False).count()

    def get_recent_tickets(self, obj):
        recent = obj.tickets.order_by('-created_at')[:5]
        return TicketSerializer(recent, many=True).data