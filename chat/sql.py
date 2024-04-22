from django.conf import settings
from django.db import connection
from django.utils.timesince import timesince


def serialize_data(cursor):
    columns = [col[0] for col in cursor.description]
    query_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return query_data


def chat_list_sql(user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_chat_list_fn(%(id)s)",
                       {'id': user_id})
        return serialize_data(cursor)


def message_list_sql(chat_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM get_message_list_fn(%(id)s)", {'id': chat_id})
        data = serialize_data(cursor)
        for message in data:
            message['human_updated_at'] = timesince(
                message.get('created_at')) + ' назад'
            if message.get('photo'):
                message['photo'] = settings.SERVER_URL + '/media/' +\
                    message['photo']

        return data
