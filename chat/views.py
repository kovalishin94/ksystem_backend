from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
from django.db.models import Q
from django.utils.timesince import timesince

from chat import sql, models, serializers
from security.models import Profile


@api_view(['GET'])
def chat_list(request):
    data = sql.chat_list_sql(request.user.id)
    for chat in data:
        chat['human_updated_at'] = timesince(chat.get('updated_at')) + ' назад'
        if chat.get('first_user_photo'):
            chat['first_user_photo'] = settings.SERVER_URL + '/media/' +\
                chat['first_user_photo']
        if chat.get('second_user_photo'):
            chat['second_user_photo'] = settings.SERVER_URL + '/media/' + \
                chat['second_user_photo']
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def chat_create(request):
    try:
        second_user = Profile.objects.get(id=request.data.get('id'))
    except:
        return Response({'message': 'Нет пользователя с данным id'}, status=status.HTTP_400_BAD_REQUEST)

    chat_query = models.Chat.objects.filter(
        Q(first_user_id=request.user.id, second_user_id=second_user.user.id) |
        Q(first_user_id=second_user.user.id, second_user_id=request.user.id))

    if chat_query.exists():
        chat_serializer = serializers.ChatSerializer(chat_query[0])
        chat_query[0].save()
        return Response(chat_serializer.data, status=status.HTTP_200_OK)

    chat = models.Chat.objects.create(
        first_user=request.user, second_user_id=second_user.user.id)
    chat_serializer = serializers.ChatSerializer(chat)

    return Response(chat_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def chat_delete(request, id):
    try:
        chat = models.Chat.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if chat.first_user != request.user and chat.second_user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    chat.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def message_list(request, id):
    if not models.Chat.objects.filter(id=id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = sql.message_list_sql(id)
    for message in data:
        message['human_updated_at'] = timesince(
            message.get('created_at')) + ' назад'
        if message.get('photo'):
            message['photo'] = settings.SERVER_URL + '/media/' +\
                message['photo']
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def message_create(request, id):
    try:
        chat = models.Chat.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if chat.first_user != request.user and chat.second_user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if not request.data.get('body'):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    message = models.Message.objects.create(
        chat=chat, created_by=request.user, body=request.data.get('body'))
    chat.save()
    photo = ''
    if message.created_by.profile.photo:
        photo = settings.SERVER_URL + '/media/' + message.created_by.profile.photo.url
    try:
        data = {
            "id": message.id,
            "body": message.body,
            "created_at": message.created_at,
            "created_by": message.created_by.profile.id,
            "photo": photo,
            "first_name": message.created_by.profile.first_name,
            "last_name": message.created_by.profile.last_name,
            "surname": message.created_by.profile.surname,
            "human_updated_at": timesince(message.created_at) + ' назад'
        }
    except:
        return Response({'message': 'Не удалось сериализовать данные'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(data, status=status.HTTP_201_CREATED)
