"""recipe.py views"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from Recipe_Core_App.models import Tag
from Recipe_API_App import serializers


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags viewset"""
    serializer_class = serializers.TagSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Tag.objects.all()

    def get_queryset(self):
        """Returns objects for authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create new tag"""
        serializer.save(user=self.request.user)
