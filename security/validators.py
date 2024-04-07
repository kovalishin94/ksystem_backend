from datetime import date

from django.core.exceptions import ValidationError


def validate_date_not_future(value):
    if value > date.today():
        raise ValidationError(
            ('Дата рождения не может быть в будущем'),
            params={'value': value},
        )