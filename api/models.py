# api/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AIConversationSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    def end_session(self):
        self.ended_at = timezone.now()
        self.save()
        
    def __str__(self):
        return f"Session {self.id} by {self.user.username}"

class AIInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(AIConversationSession, on_delete=models.CASCADE)
    input = models.TextField()  
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Interaction {self.id} in Session {self.session.id}"
