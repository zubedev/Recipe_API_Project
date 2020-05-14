"""recipe.py serializer"""

from rest_framework import serializers

from Recipe_Core_App.models import Tag, Ingredient, Recipe


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


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe object"""
    ingredients = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        """Meta class"""
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags', 'duration', 'price',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize detailed recipe"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes"""

    class Meta:
        """Meta class"""
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id', )
