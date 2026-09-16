from django.urls import path
from .views import ( 
    AIAgentListView, 
    AIAgentDetailtView,
    AIAgentCreateView,
    AIAgentUpdateView,
    AIAgentDeletetView,
    UserAIAgentListView
)
from . import views 

urlpatterns = [
    path('',AIAgentListView.as_view(), name='home-AI-Agents'),
    path('user/<str:username>', UserAIAgentListView.as_view(), name='user-aiagent'),
    path('<int:pk>/', AIAgentDetailtView.as_view(), name='ai_agent_detail'),
    path('new/', AIAgentCreateView.as_view(), name='aiagent-create'),
    path('<int:pk>/update/', AIAgentUpdateView.as_view(), name='aiagent-update'),
    path('<int:pk>/delete/', AIAgentDeletetView.as_view(), name='aiagent-delete'),
    path('<int:pk>/discuss/', views.discussWithAgentAI, name='aiagent-discuss'),
    path("agent/<int:pk>/chat-data/", views.fetch_chat_data, name="fetch_chat_data"),
    path('helb_plays2025/', views.helb_plays2025, name='helb_plays2025'),
    path('chat/', views.get_chat, name='chat'),
    path('send_chat/', views.send_message_helb_plays2025, name='send_chat'),
]