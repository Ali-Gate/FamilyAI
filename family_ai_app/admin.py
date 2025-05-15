from django.contrib import admin
from .models import Ticket, Message, Notification

# Register your models here.

admin.site.register(Ticket)

admin.site.register(Message)

admin.site.register(Notification)