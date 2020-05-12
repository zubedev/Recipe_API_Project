"""Custom User Model"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """Custom User Manager overridden from BaseUserManager for CustomUser"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a new user using an email address"""
        if not email:  # check for an empty email
            raise ValueError("User must set an email address")
        else:  # normalizes the provided email
            email = self.normalize_email(email)
        # set defaults
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # create user
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes/encrypts password
        user.save(using=self._db)  # safe for multiple databases
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True, blank=False,
                              null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField('Staff status', default=False, null=True)
    is_active = models.BooleanField('Active', default=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    objects = CustomUserManager()  # uses the custom manager

    USERNAME_FIELD = 'email'  # overrides username to email field
