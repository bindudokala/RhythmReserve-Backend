from .models import ChatSession, Message
from .serializers import ChatSessionSerializer, MessageSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import JsonResponse

class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['get'])
    def by_username(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'Username not provided'}, status=status.HTTP_400_BAD_REQUEST)

        session, created = ChatSession.objects.get_or_create(user_name=username)
        messages = Message.objects.filter(session=session).order_by('-created_at')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    


def fetch_all_chats(request):
    # Assuming each ChatSession has a related_name 'messages' to the Message model
    chat_sessions = ChatSession.objects.prefetch_related('messages').all()
    chats_data = []

    for session in chat_sessions:
        messages = session.messages.order_by('created_at')
        chats_data.append({
            'session_id': session.id,
            'user_name': session.user_name,
            'messages': [{
                'id': message.id,
                'text': message.text,
                'sender': message.sender,
                'created_at': message.created_at,
            } for message in messages]
        })

    return JsonResponse(chats_data, safe=False)  # Set safe=False for non-dict objects

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatSession
from .serializers import ChatSessionSerializer

class ChatSessionDetailView(APIView):
    def get(self, request, session_id):
        try:
            session = ChatSession.objects.prefetch_related('messages').get(pk=session_id)
            serializer = ChatSessionSerializer(session)
            return Response(serializer.data)
        except ChatSession.DoesNotExist:
            return Response({'error': 'Chat session not found'}, status=404)
        

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatSession, Message
from .serializers import MessageSerializer

class SessionMessagesView(APIView):
    def get(self, request, session_id):
        try:
            session = ChatSession.objects.get(pk=session_id)
            messages = session.messages.order_by('created_at')
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except ChatSession.DoesNotExist:
            return Response({'error': 'Chat session not found'}, status=status.HTTP_404_NOT_FOUND)
        

class SessionCreateAPIView(APIView):
    def post(self, request):
        serializer = ChatSessionSerializer(data=request.data)
        if serializer.is_valid():
            session = serializer.save()
            return Response({'id': session.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
