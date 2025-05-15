from django.urls import path
from .views import AIConversationView, EndConversationView

urlpatterns = [
    path('conversation/', AIConversationView.as_view(), name='ai-conversation'),
    path('end-conversation/', EndConversationView.as_view(), name='end-conversation'),
]