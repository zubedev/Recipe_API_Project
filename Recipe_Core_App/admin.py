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


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin for Tag model"""
    model = models.Tag
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('name', 'user', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', )
    search_fields = ('id', 'name', 'user')
    ordering = ('name', 'user', 'created_at', 'updated_at')
