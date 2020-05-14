"""custom_user.py serializer"""

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import BaseUserManager

from rest_framework import serializers

USER_MODEL = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for the Custom User object"""

    class Meta:
        """Meta class"""
        model = USER_MODEL
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Creates and returns a new user with encrypted password"""
        return USER_MODEL.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Updates and returns the user, sets the password correctly"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Token authentication overridden for Custom User object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False  # password can contain whitespace
    )

    def validate(self, attrs):
        """token validation and authentication"""
        email = BaseUserManager.normalize_email(attrs.get('email'))
        user = authenticate(
            request=self.context.get('request'),
            username=email,  # email as username for custom user
            password=attrs.get('password')
        )
        if not user:
            msg = "Unable to authenticate user with provided credentials"
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs
