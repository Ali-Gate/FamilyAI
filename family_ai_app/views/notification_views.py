from rest_framework import generics, permissions
from family_ai_app.models import Notification
from family_ai_app.serializers import NotificationSerializer
from family_ai_app.permissions import IsOwnerOfNotification

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfNotification]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)