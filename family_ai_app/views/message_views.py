from rest_framework import generics, permissions, status
from rest_framework.response import Response
from family_ai_app.models import Message
from family_ai_app.serializers import MessageSerializer
from family_ai_app.permissions import IsSenderOrAdmin

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        ticket_id = self.request.query_params.get('ticket_id')
        queryset = Message.objects.all() if user.is_staff or user.is_superuser else Message.objects.filter(sender=user)

        if ticket_id:
            queryset = queryset.filter(ticket__id=ticket_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsSenderOrAdmin]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.all() if user.is_staff or user.is_superuser else Message.objects.filter(sender=user)

    def perform_update(self, serializer):
        serializer.validated_data.pop('sender', None)
        serializer.save()

    def put(self, request, *args, **kwargs):
        return self._update_response(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self._update_response(request, partial=True, *args, **kwargs)

    def _update_response(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)