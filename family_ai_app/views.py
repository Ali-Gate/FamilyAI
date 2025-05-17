from django.shortcuts import render, redirect
from allauth.account.views import SignupView
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from family_ai_app.models import Ticket, Message
from family_ai_app.serializers import TicketSerializer, MessageSerializer, UserSerializer
from family_ai_app.permissions import IsOwnerOrAdmin, IsSenderOrAdmin

# Create your views here.


def home(request):
    return render(request, 'family_ai/home.html')

def login_redirect(request):
    return redirect('account_login')

def logout_redirect(request):
    return redirect('account_logout')

def register_redirect(request):
    return redirect('account_signup')


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


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

class TicketDetailView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=user)


class TicketDeleteView(generics.DestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(sender=user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsSenderOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(sender=user)
    

class CustomSignupView(SignupView):
    def form_valid(self, form):
        response = super().form_valid(form)
        # Logout the user immediately after sign-up
        from django.contrib.auth import logout
        logout(self.request)
        return redirect('/accounts/login/')  # redirects to login page