"""custom_user.py view"""

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from Recipe_API_App.serializers import CustomUserSerializer, \
    AuthTokenSerializer


class CreateCustomUserView(generics.CreateAPIView):
    """Creates a new user"""
    serializer_class = CustomUserSerializer


class CreateTokenView(ObtainAuthToken):
    """Creates a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
