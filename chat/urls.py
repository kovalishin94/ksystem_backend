from django.urls import path

from chat import views


urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('create/', views.chat_create, name='chat_create'),
    path('<uuid:id>/', views.message_list, name='message_list'),
    path('<uuid:id>/delete/', views.chat_delete, name='chat_delete'),
    path('<uuid:id>/send/', views.message_create, name='message_create'),
]
