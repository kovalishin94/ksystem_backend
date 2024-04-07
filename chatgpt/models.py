import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timesince import timesince


class ChatQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='chatquestions')
    body = models.TextField()
    bot_role = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ChatAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    answer = models.TextField()
    question = models.OneToOneField(
        ChatQuestion, on_delete=models.CASCADE, related_name='answer')
    speech = models.FileField(upload_to='gpt_speeches/', blank=True, null=True)
    image = models.ImageField(upload_to='gpt_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def speech_url(self):
        if self.speech:
            return settings.SERVER_URL + self.speech.url
        else:
            return ''

    def image_url(self):
        if self.image:
            return settings.SERVER_URL + self.image.url
        else:
            return ''

    def human_created_at(self):
        return timesince(self.created_at) + ' назад'

    class Meta:
        ordering = ['-created_at']
