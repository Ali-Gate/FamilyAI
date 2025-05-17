from rest_framework import generics, permissions, status
from rest_framework.response import Response
from family_ai_app.models import Ticket
from family_ai_app.serializers import TicketSerializer
from family_ai_app.serializers.ticket import AssignAdminSerializer
from family_ai_app.permissions import IsOwnerOrAdmin
from django.contrib.auth.models import User
from family_ai_app.models import Notification

class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Ticket.objects.all().order_by('-created_at')
        return Ticket.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)

class TicketDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=user)

    def perform_update(self, serializer):
        previous_admin = serializer.instance.assigned_admin
        ticket = serializer.save()

        new_admin = ticket.assigned_admin
        if new_admin and new_admin != previous_admin:
            # Remove notifications for other admins for this ticket
            other_admins = User.objects.filter(is_staff=True).exclude(id=new_admin.id)
            Notification.objects.filter(ticket=ticket, user__in=other_admins).delete()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)

class TicketDeleteView(generics.DestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"detail": "Ticket deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class AssignSelfToTicketView(generics.UpdateAPIView):
    serializer_class = AssignAdminSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Ticket.objects.all()
    lookup_url_kwarg = 'pk'

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()

        # Use the serializer, but override assigned_admin forcibly in serializer.update()
        serializer = self.get_serializer(ticket, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Remove notifications for other admins
        other_admins = User.objects.filter(is_staff=True).exclude(id=request.user.id)
        Notification.objects.filter(ticket=ticket, user__in=other_admins).delete()

        return Response(
            {"detail": f"Assigned admin user {request.user.username} to ticket #{ticket.pk}."},
            status=status.HTTP_200_OK
        )