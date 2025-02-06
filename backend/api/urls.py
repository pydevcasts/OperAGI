from django.urls import path
from .views import  transcribe_audio,get_answer
app_name = "api"


urlpatterns = [
    path('transcribe/', transcribe_audio, name='transcribe_audio'),
    path('get_answer/', get_answer, name='get_answer'),
]