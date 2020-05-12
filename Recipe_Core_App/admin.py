"""Django Admin for Recipe_Core_App"""

from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from Recipe_Core_App import models


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin for CustomUser model"""
    ordering = ('name', 'email')
    list_display = ('name', 'email', 'last_login', 'date_joined', 'is_staff',
                    'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', )}),
        ('Roles', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('name', 'email', 'password1', 'password2')
        }),
    )
    readonly_fields = ('last_login', 'date_joined')
