from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserSocialAccount
from .serializers import UserSocialAccountSerializer


class UserSocialAccountViewSet(viewsets.ModelViewSet):
    serializer_class = UserSocialAccountSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return UserSocialAccount.objects.none()
        return UserSocialAccount.objects.filter(user=self.request.user).select_related('social_account')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
