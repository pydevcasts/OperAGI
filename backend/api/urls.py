from django.urls import path
from .views import TranscribeAudioView, chat_completion

app_name = "api"

urlpatterns = [
    path('', TranscribeAudioView.as_view(), name='transcribe_audio'),
    path('chat/', chat_completion, name='chat_completion'),
]
