"""recipe.py serializer"""

from rest_framework import serializers

from Recipe_Core_App.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag object"""

    class Meta:
        """Meta class"""
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id', )
