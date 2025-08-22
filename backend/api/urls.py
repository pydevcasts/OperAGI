from django.urls import path
from .views import TranscribeAudioView, health_check,ChatCompletionView

urlpatterns = [
    path('transcribe/', TranscribeAudioView.as_view(), name='transcribe'),
    path('openai/completion/', ChatCompletionView.as_view(), name='openai-completion'),
    path('health/', health_check, name='health_check'),
]