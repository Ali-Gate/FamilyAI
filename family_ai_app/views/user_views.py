from django.contrib.auth.models import User
from rest_framework import generics, permissions
from family_ai_app.serializers import UserSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
