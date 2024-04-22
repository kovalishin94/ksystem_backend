import json

from django.conf import settings
from django.utils.timesince import timesince

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .sql import message_list_sql
from .models import Message, Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        self.messages = await sync_to_async(message_list_sql)(self.room_name)

        await self.send(text_data=json.dumps(self.messages, default=str))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = ''

        if text_data_json.get('close'):
            await self.close()

        if text_data_json.get('body'):
            message = await self.create_message(text_data_json.get('body'))

        if message:
            await self.channel_layer.group_send(self.room_group_name, {'type': 'send.message', 'message': message})

    async def send_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps(message, default=str))

    @database_sync_to_async
    def create_message(self, body):
        if not body:
            return

        try:
            chat = Chat.objects.get(id=self.room_name)
        except:
            return

        message = Message.objects.create(
            chat_id=self.room_name, created_by=self.scope['user'], body=body)
        chat.save()
        photo = ''
        if message.created_by.profile.photo:
            photo = settings.SERVER_URL + '/media/' + message.created_by.profile.photo.url
        try:
            return {
                "id": str(message.id),
                "body": message.body,
                "created_at": str(message.created_at),
                "created_by": str(message.created_by.profile.id),
                "photo": photo,
                "first_name": message.created_by.profile.first_name,
                "last_name": message.created_by.profile.last_name,
                "surname": message.created_by.profile.surname,
                "human_updated_at": timesince(message.created_at) + ' назад'
            }
        except:
            return
