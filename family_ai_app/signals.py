from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from family_ai_app.models import Ticket, Notification, Message

User = get_user_model()

@receiver(post_save, sender=Ticket)
def notify_admins_on_ticket_creation(sender, instance, created, **kwargs):
    if created:
        admins = User.objects.filter(is_staff=True, is_active=True)
        for admin in admins:
            Notification.objects.create(
                user=admin,
                ticket=instance,
                title=f"New ticket created: '{instance.subject}'",
                description=f"Ticket created by {instance.user}",
            )

@receiver(post_save, sender=Message)
def notify_ticket_users_on_message(sender, instance, created, **kwargs):
    if created:
        ticket = instance.ticket
        sender_user = instance.sender

        users_to_notify = set()

        # Add ticket owner if not sender
        if ticket.user != sender_user:
            users_to_notify.add(ticket.user)

        if ticket.assigned_admin:
            # Notify only the assigned admin if they are not the sender
            if ticket.assigned_admin != sender_user:
                users_to_notify.add(ticket.assigned_admin)
        else:
            # Notify all active staff admins except the sender
            admins = User.objects.filter(is_staff=True, is_active=True).exclude(id=sender_user.id)
            users_to_notify.update(admins)

        notifications = [
            Notification(
                user=user,
                ticket=ticket,
                message=instance,  # Link actual Message instance here
                title=f'New message on ticket: {ticket.subject}',
                description=instance.message,
                is_seen=False,
            )
            for user in users_to_notify
        ]

        Notification.objects.bulk_create(notifications)