from rest_framework import serializers
from family_ai_app.models import Notification
from django.utils import timezone

class NotificationSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    ticket_id = serializers.IntegerField(source='ticket.id', read_only=True)
    message_id = serializers.IntegerField(source='message.id', read_only=True)
    is_seen = serializers.BooleanField(read_only=True)
    seen_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    # New field to show the ticket creator's username
    ticket_creator = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'user_username',
            'ticket_creator',
            'ticket',
            'ticket_id',
            'message',
            'message_id',
            'title',
            'description',
            'is_seen',
            'seen_at',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'user_username',
            'ticket_creator',
            'ticket_id',
            'message_id',
            'is_seen',
            'seen_at',
            'created_at',
        ]

    def get_ticket_creator(self, obj):
        if obj.ticket and obj.ticket.user:
            return obj.ticket.user.username
        return None

    def mark_as_seen(self):
        """Optionally, if you want to expose mark_as_seen in serializer context."""
        instance = self.instance
        if instance and not instance.is_seen:
            instance.is_seen = True
            instance.seen_at = timezone.now()
            instance.save()
