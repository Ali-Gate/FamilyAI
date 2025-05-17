from django.urls import path
from . import views
from .views import (
    UserListView,
    TicketListCreateView,
    TicketDetailView,
    TicketDeleteView,
    MessageListCreateView,
    MessageDetailView,
    # Placeholder for future Notification views
)


app_name = 'family_ai_app'
# The app_name is used to create namespaced URLs for the app.


# The urlpatterns list routes URLs to views
urlpatterns = [
    # Navigation endpoints
    path('', views.home, name='home'),

    # User endpoints
    path('users/', UserListView.as_view(), name='user-list'),

    # Ticket endpoints
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),

    # Message endpoints
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
]
