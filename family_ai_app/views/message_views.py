from rest_framework import generics, permissions
from family_ai_app.models import Message
from family_ai_app.serializers import MessageSerializer
from family_ai_app.permissions import IsSenderOrAdmin

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.all() if user.is_staff or user.is_superuser else Message.objects.filter(sender=user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsSenderOrAdmin]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.all() if user.is_staff or user.is_superuser else Message.objects.filter(sender=user)

    def perform_update(self, serializer):
        serializer.validated_data.pop('sender', None)
        serializer.save()

