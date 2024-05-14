from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from .views import SessionCreateAPIView, ChatSessionDetailView

router = DefaultRouter()
router.register(r'sessions', views.ChatSessionViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/chats/', views.fetch_all_chats, name='fetch_all_chats'),
    path('api/sessions/', SessionCreateAPIView.as_view(), name='create_session'),
    path('api/messages/session/<int:session_id>/', views.SessionMessagesView.as_view(), name='session_messages'),
    path('api/chat_sessions/<int:session_id>/', ChatSessionDetailView.as_view(), name='chat_session_detail'),
]

