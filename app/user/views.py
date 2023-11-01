"""Views for User API"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthtokenSerializer,
)


class CreateUserViwe(generics.CreateAPIView):
    """View for create user"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create auth token view."""
    serializer_class = AuthtokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
