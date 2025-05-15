from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import AIInteraction, AIConversationSession
from .serializers import AIInteractionSerializer
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

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

        # Generate AI response
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a patient, kind assistant helping family members with technical issues. Provide simple, step-by-step instructions suitable for all ages."},
                    {"role": "user", "content": f"Explain this in very simple terms: {user_input}"}
                ],
                temperature=0.5,
                max_tokens=500
            )

            ai_response = response.choices[0].message['content'].strip()

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
