from django.contrib import admin
from chat.models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_user',
        'second_user',
        'created_at',
        'updated_at',
    )

    list_display_links = (
        'id',
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'chat',
        'created_by',
        'body',
        'created_at',
    )

    list_display_links = (
        'id',
    )
