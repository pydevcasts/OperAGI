from django.urls import path
from .views import  TranscribeAudioView

app_name = "api"


urlpatterns = [
    path('', TranscribeAudioView.as_view(), name='transcribe_audio'),
    
]

