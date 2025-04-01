from django.urls import path
from .views import TranscribeAudioView, DeepSeekResponseView,health_check

urlpatterns = [
    path('transcribe/', TranscribeAudioView.as_view(), name='transcribe'),
    path('chat/', DeepSeekResponseView.as_view(), name='chat'),
    path('health/', health_check, name='health_check'),
]