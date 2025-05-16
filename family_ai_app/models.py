from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Ticket(models.Model):
    # Choices for ticket status
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
    ]

    # The user who created the ticket
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')

    # Subject or title of the support ticket
    subject = models.CharField(max_length=255)

    # Current status of the ticket
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')

    # Timestamp when the ticket was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp when the ticket was last updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # String representation for readability in admin or logs
        return f"Ticket #{self.id} - {self.subject}"


class Message(models.Model):
    # Reference to the ticket this message is part of
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')

    # The user who sent the message
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    # The content of the message
    message = models.TextField()

    # Whether the message has been read
    is_read = models.BooleanField(default=False)

    # Timestamp of when the message was read
    read_at = models.DateTimeField(null=True, blank=True)

    # Timestamp when the message was created
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        # Marks the message as read and sets the read timestamp
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

    def __str__(self):
        # String representation for readability in admin or logs
        return f"Message by {self.sender.username} on Ticket #{self.ticket.id}"


class Notification(models.Model):
    # The user who receives the notification
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    # Optional reference to a related ticket
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, null=True, blank=True)

    # Optional reference to a related message
    message = models.ForeignKey('Message', on_delete=models.CASCADE, null=True, blank=True)

    # Title of the notification
    title = models.CharField(max_length=255)

    # Additional information or context for the notification
    description = models.TextField(blank=True)

    # Whether the notification has been seen
    is_seen = models.BooleanField(default=False)

    # Timestamp of when the notification was seen
    seen_at = models.DateTimeField(null=True, blank=True)

    # Timestamp when the notification was created
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_seen(self):
        # Marks the notification as seen and sets the seen timestamp
        if not self.is_seen:
            self.is_seen = True
            self.seen_at = timezone.now()
            self.save()

    def __str__(self):
        # String representation for readability in admin or logs
        return f"Notification for {self.user.username} - {self.title}"