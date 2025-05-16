from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import AIInteraction, AIConversationSession
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import AIInteractionSerializer
import os
from openai import OpenAI 


# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AIConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get or create active session
        session, created = AIConversationSession.objects.get_or_create(
            user=request.user,
            ended_at__isnull=True
        )

        user_input = request.data.get('input', '')
        if not user_input:
            return Response({"error": "Input cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate AI response using new API format
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Please assist the user but make sure you make the instructions in step by step format and very easy to follow as the user might be elderly or a child"},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.5,
                max_tokens=500
            )

            ai_response = response.choices[0].message.content  

            # Save interaction
            interaction = AIInteraction.objects.create(
                user=request.user,
                session=session,
                input=user_input,
                response=ai_response
            )

            return Response(AIInteractionSerializer(interaction).data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EndConversationView(APIView):

    permission_classes = [IsAuthenticated] 

    def post(self, request):
        session = AIConversationSession.objects.filter(
            user=request.user,
            ended_at__isnull=True
        ).first()

        if session:
            session.end_session()
            return Response({"status": "Session ended"})
        return Response({"error": "No active session"}, status=status.HTTP_400_BAD_REQUEST)
