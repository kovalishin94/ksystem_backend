from django.db import connection

def serialize_data(cursor):
    columns = [col[0] for col in cursor.description]
    query_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return query_data

def chat_list_sql(user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_chat_list_fn(%(id)s)", {'id': user_id})
        return serialize_data(cursor)
    
def message_list_sql(chat_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_message_list_fn(%(id)s)", {'id': chat_id})
        return serialize_data(cursor)