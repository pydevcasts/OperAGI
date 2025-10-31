# from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from django.urls import path
from .views import GoogleLoginView

urlpatterns = [
    path('', GoogleLoginView.as_view(), name='google_login'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

