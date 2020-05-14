"""Recipe Core App - recipe.py models"""

from django.conf import settings
from django.db import models


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255, unique=True, blank=False,
                            null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,
                             on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField('Active', default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """Tag string representation"""
        return self.name
