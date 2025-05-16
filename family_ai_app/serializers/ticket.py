from rest_framework import serializers
from family_ai_app.models import Ticket
from .message import MessageSerializer

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
        read_only_fields = [
            'id', 'user', 'created_at', 'updated_at',
            'messages_count', 'status_display', 'messages'
        ]

    def get_messages_count(self, obj):
        return obj.messages.count()

    def get_status_display(self, obj):
        return obj.get_status_display()

    def create(self, validated_data):
        # Always force status to 'open' on create regardless of input
        validated_data['status'] = 'open'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        # Only staff or superusers can change status
        if 'status' in validated_data:
            if not (request and request.user and (request.user.is_staff or request.user.is_superuser)):
                validated_data.pop('status')  # Remove status change for non-staff users
        return super().update(instance, validated_data)

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        # Make 'status' read-only for non-staff users so they don't even see it as writable in the serializer
        if request and not (request.user.is_staff or request.user.is_superuser):
            fields['status'].read_only = True
        return fields