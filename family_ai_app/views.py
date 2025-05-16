from django.shortcuts import render
from rest_framework import generics, permissions
from family_ai_app.models import Ticket
from family_ai_app.serializers import TicketSerializer
from family_ai_app.permissions import IsOwnerOrAdmin

# Create your views here.


def home(request):
    return render(request, 'family_ai/home.html')


class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Admins see all tickets; regular users only their own
        if user.is_staff or user.is_superuser:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketDeleteView(generics.DestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]