import os
import datetime
import openai
import requests

from dotenv import load_dotenv

from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from chatgpt import models, serializers

load_dotenv()
openai.api_key = os.getenv("OPENAI_TOKEN")


def create_db_entry(user_pk, question_body, bot_role, answer, speech=None, image=None):
    chat_question_serialiser = serializers.ChatQuestionSerializer(
        data={
            'user': user_pk,
            'body': question_body,
            'bot_role': bot_role
        }
    )
    if chat_question_serialiser.is_valid():
        chat_question = chat_question_serialiser.save()
    else:
        return Response({'message': 'ChatQuestionSerializer не прошел валидацию!'}, status.HTTP_400_BAD_REQUEST)

    chat_answer_serializer = serializers.ChatAnswerSerializer(
        data={
            'answer': answer,
            'question': chat_question.pk
        }
    )

    if chat_answer_serializer.is_valid():
        chat_answer = chat_answer_serializer.save()
    else:
        chat_question.delete()
        return Response({'message': 'ChatAnswerSerializer не прошел валидацию!'}, status.HTTP_400_BAD_REQUEST)

    if speech:
        try:
            chat_answer.speech.name = speech
            chat_answer.save()
        except:
            chat_answer.delete()
            chat_question.delete()
            return Response({'message': 'Не удалось сделать записать путь к файлу в базу данных'}, status.HTTP_400_BAD_REQUEST)

    if image:
        try:
            chat_answer.image.name = image
            chat_answer.save()
        except:
            chat_answer.delete()
            chat_question.delete()
            return Response({'message': 'Не удалось сделать записать путь к файлу в базу данных'}, status.HTTP_400_BAD_REQUEST)

    response_serializer = serializers.ChatSerializer(chat_answer)

    return Response(response_serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def get_chat_messages(request):
    queryset = models.ChatAnswer.objects.filter(question__user=request.user)
    response_serializer = serializers.ChatSerializer(queryset, many=True)

    return Response(response_serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def gpt(request):
    if not request.data.get('chatquestion'):
        return Response({'message': 'Нет данных для отправки'}, status.HTTP_400_BAD_REQUEST)

    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "assistant",
                 "content": request.data.get('chatquestion')
                 }
            ]
        )
        answer = completion.choices[0].message.content
        return create_db_entry(request.user.pk, request.data.get(
            'chatquestion'), 'gpt-3.5-turbo', answer)

    except:
        return Response({'message': 'Ошибка обращения к серверу OpenAI'}, status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def dalle(request):
    if not request.data.get('chatquestion'):
        return Response({'message': 'Нет данных для отправки'}, status.HTTP_400_BAD_REQUEST)
    now = datetime.datetime.now()
    try:
        response = openai.images.generate(
            model="dall-e-2",
            prompt=request.data.get('chatquestion'),
            size="1024x1024",
            quality="standard",
            n=1)
        url = response.data[0].url
        speech_file_path = f'gpt_images/{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.png'
        speech_full_file_path = settings.MEDIA_ROOT / speech_file_path
        resource = requests.get(url)
        with open(speech_full_file_path, 'wb') as f:
            f.write(resource.content)

        return create_db_entry(request.user.pk, request.data.get(
            'chatquestion'), 'dall-e-2', 'Фото', image=speech_file_path)

    except:
        return Response({'message': 'Ошибка обращения к серверу OpenAI'}, status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def tts(request):
    if not request.data.get('chatquestion'):
        return Response({'message': 'Нет данных для отправки'}, status.HTTP_400_BAD_REQUEST)

    now = datetime.datetime.now()

    try:
        speech_file_path = f'gpt_speeches/speech-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.mp3'
        speech_full_file_path = settings.MEDIA_ROOT / speech_file_path
        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=request.data.get('chatquestion')
        )
        response.stream_to_file(speech_full_file_path)

        return create_db_entry(request.user.pk, request.data.get(
            'chatquestion'), 'tts-1', 'Аудио', speech=str(speech_file_path))

    except:
        return Response({'message': 'Ошибка обращения к серверу OpenAI'}, status.HTTP_503_SERVICE_UNAVAILABLE)
