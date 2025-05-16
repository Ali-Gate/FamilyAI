from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.subject}"
    

class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)  # 🔹 Timestamp added
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

    def __str__(self):
        return f"Message by {self.sender.username} on Ticket #{self.ticket.id}"
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, null=True, blank=True)
    message = models.ForeignKey('Message', on_delete=models.CASCADE, null=True, blank=True)
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    is_seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_seen(self):
        if not self.is_seen:
            self.is_seen = True
            self.seen_at = timezone.now()
            self.save()

    def __str__(self):
        return f"Notification for {self.user.username} - {self.title}"