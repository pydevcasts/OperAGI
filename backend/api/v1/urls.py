from django.urls import path, include

urlpatterns = [
    path('user/', include('accounts.urls')),
    path('documents/', include('documents.urls')),
    path('embeddings/', include('embeddings.urls')),
    path('qa/', include('qa.urls')),
]