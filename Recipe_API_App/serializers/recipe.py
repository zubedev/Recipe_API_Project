"""recipe.py serializer"""

from rest_framework import serializers

from Recipe_Core_App.models import Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag object"""

    class Meta:
        """Meta class"""
        model = Tag
        fields = ('id', 'name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient object"""

    class Meta:
        """Meta class"""
        model = Ingredient
        fields = ('id', 'name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
