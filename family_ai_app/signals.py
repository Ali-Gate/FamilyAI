from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from family_ai_app.models import Ticket, Notification, Message

User = get_user_model()

@receiver(post_save, sender=Ticket)
def notify_admins_on_ticket_creation(sender, instance, created, **kwargs):
    if created:
        admins = User.objects.filter(is_staff=True, is_active=True)
        notifications = [
            Notification(
                user=admin,
                ticket=instance,
                message=f"New ticket created: '{instance.subject}' by {instance.user}"
            )
            for admin in admins
        ]
        Notification.objects.bulk_create(notifications)


@receiver(post_save, sender=Message)
def notify_ticket_users_on_message(sender, instance, created, **kwargs):
    if not created:
        return

    ticket = instance.ticket
    sender_user = instance.sender

    # Users linked to the ticket excluding the sender
    ticket_owner = ticket.user
    admins = User.objects.filter(is_staff=True, is_active=True)

    # Combine ticket owner and admins, exclude sender
    users_to_notify = {user for user in admins}
    if ticket_owner != sender_user:
        users_to_notify.add(ticket_owner)
    users_to_notify.discard(sender_user)

    notifications = [
        Notification(
            user=user,
            ticket=ticket,
            message=f"New message on ticket: {ticket.subject}",
            is_read=False,
        )
        for user in users_to_notify
    ]

    Notification.objects.bulk_create(notifications)