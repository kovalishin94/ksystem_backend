from django.contrib import admin

from .models import ChatAnswer, ChatQuestion

@admin.register(ChatAnswer)
class ChatAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'answer',
        'question',
    )    

    list_display_links = (
        'id',
    )

@admin.register(ChatQuestion)
class ChatQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'body',
        'bot_role',
        'created_at',
    )

    list_display_links = (
        'id',        
    )

