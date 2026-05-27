# backend\accounts\views.py (کنار ویوهای لاگین)

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from .models import UserSocialAccount
from .serializers import UserSocialAccountSerializer


class UserSocialAccountViewSet(viewsets.ModelViewSet):
    serializer_class = UserSocialAccountSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        return UserSocialAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # Pass user to serializer's save, which then passes to create context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() 
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

