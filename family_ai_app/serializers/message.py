from rest_framework import serializers
from . import user  # if you need user serializers later (optional)
from family_ai_app.models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    ticket_id = serializers.IntegerField(source='ticket.id', read_only=True)
    is_read = serializers.BooleanField(read_only=True)
    read_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    ticket_title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'ticket',
            'ticket_id',
            'ticket_title',
            'sender',
            'sender_username',
            'message',
            'is_read',
            'read_at',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'ticket_id',
            'sender',
            'sender_username',
            'is_read',
            'read_at',
            'created_at',
            'ticket_title',
        ]

    def get_ticket_title(self, obj):
        # This assumes the Ticket model has a `title` field
        return obj.ticket.subject if obj.ticket and hasattr(obj.ticket, 'subject') else None

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message content cannot be empty.")
        return value