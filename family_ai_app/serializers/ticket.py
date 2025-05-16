from rest_framework import serializers
from family_ai_app.models import Ticket
from .message import MessageSerializer  # import MessageSerializer

class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    messages_count = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'user',
            'subject',
            'status',
            'status_display',
            'messages_count',
            'messages',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'messages_count', 'status_display', 'messages']

    def get_messages_count(self, obj):
        return obj.messages.count()

    def get_status_display(self, obj):
        return obj.get_status_display()