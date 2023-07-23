from rest_framework.validators import ValidationError


def validate_tags(data):
    """Валидация тэгов: отсутствие в request, отсутствие в БД."""
    if not data:
        raise ValidationError({'tags': ['Обязательное поле.']})
    return data
