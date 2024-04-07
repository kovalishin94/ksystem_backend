from django.contrib import admin
from .models import Permission, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'email',
        'first_name'
    )

    list_display_links = (
        'id',
        'user'
    )

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )

    list_display_links = (
        'id',
        'name'
    )
