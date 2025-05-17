from django.contrib.auth.models import User
from rest_framework import serializers
from family_ai_app.models import Ticket
from .message import MessageSerializer

class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    assigned_admin = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_staff=True), required=False, allow_null=True
    )
    messages_count = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'user', 'assigned_admin', 'subject', 'status',
            'status_display', 'messages_count', 'messages',
            'created_at', 'updated_at',
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
                validated_data.pop('status')

        # Only staff or superusers can assign or change assigned_admin
        if 'assigned_admin' in validated_data:
            if not (request and request.user and (request.user.is_staff or request.user.is_superuser)):
                validated_data.pop('assigned_admin')

        return super().update(instance, validated_data)

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')

        # Make 'status' read-only for non-staff users so they don't see it writable
        if request and not (request.user.is_staff or request.user.is_superuser):
            fields['status'].read_only = True
            fields['assigned_admin'].read_only = True  # Also hide assigned_admin from non-staff users

        return fields


class AssignAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['assigned_admin']

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_staff:
            instance.assigned_admin = request.user  # force assign self, ignore input
        else:
            # fallback to input or keep existing assigned_admin
            instance.assigned_admin = validated_data.get('assigned_admin', instance.assigned_admin)
        instance.save()
        return instance