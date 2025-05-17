from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth.models import User
from rest_framework import serializers
from family_ai_app.models import Ticket
from .message import MessageSerializer

class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    assigned_admin_id = serializers.PrimaryKeyRelatedField(
        source='assigned_admin',
        queryset=User.objects.filter(is_staff=True),
        required=False,
        allow_null=True,
        write_only=True
    )
    assigned_admin = serializers.SerializerMethodField()
    messages_count = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'user', 'assigned_admin_id', 'assigned_admin',
            'subject', 'status', 'status_display', 'created_at', 'updated_at',
            'messages_count', 'messages', 
        ]
        read_only_fields = [
            'id', 'user', 'created_at', 'updated_at',
            'messages_count', 'status_display', 'messages', 'assigned_admin'
        ]

    def get_assigned_admin(self, obj):
        return obj.assigned_admin.username if obj.assigned_admin else None

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

        # Hide assignable fields from non-staff users
        if request and not (request.user.is_staff or request.user.is_superuser):
            fields['status'].read_only = True
            fields['assigned_admin_id'].read_only = True

        return fields
    
    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)


class AssignAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['assigned_admin']

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_staff:
            instance.assigned_admin = request.user  # force assign self
        else:
            instance.assigned_admin = validated_data.get('assigned_admin', instance.assigned_admin)
        instance.save()
        return instance
