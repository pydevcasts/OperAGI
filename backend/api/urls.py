from django.urls import path
from .views import TranscribeAudioView, chat_with_deepseek 

app_name = "api"

urlpatterns = [
    path('', TranscribeAudioView.as_view(), name='transcribe_audio'),
    path('chat/', chat_with_deepseek, name='chat_with_deepseek'),
]
