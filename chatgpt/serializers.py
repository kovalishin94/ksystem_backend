from rest_framework import serializers

from chatgpt import models


class ChatQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatQuestion
        fields = (
            'user',
            'body',
            'bot_role'
        )


class ChatAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatAnswer
        fields = (
            'answer',
            'question'
        )


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatAnswer
        fields = (
            'id',
            'answer',
            'human_created_at',
            'question',
            'speech_url',
            'image_url'
        )
        depth = 1
