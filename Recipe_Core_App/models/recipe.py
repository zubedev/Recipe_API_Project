"""Recipe Core App - recipe.py models"""

import os
import uuid

from django.conf import settings
from django.db import models


def recipe_image_file_path(instance, filename):
    """Generate file path for recipe image"""
    ext = filename.split('.')[-1]  # get the file extension
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('recipe/', filename)


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    is_active = models.BooleanField('Active', default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """Tag string representation"""
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used for a recipe"""
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    is_active = models.BooleanField('Active', default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """Ingredient string representation"""
        return self.name


class Recipe(models.Model):
    """Recipe model"""
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)
    duration = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to=recipe_image_file_path, null=True)
    is_active = models.BooleanField('Active', default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """Recipe string representation"""
        return self.title
