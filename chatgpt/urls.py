from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_chat_messages, name='get_chat_messages'),
    path('gpt/', views.gpt, name='gpt'),
    path('dalle/', views.dalle, name='dalle'),
    path('tts/', views.tts, name='tts')
]
