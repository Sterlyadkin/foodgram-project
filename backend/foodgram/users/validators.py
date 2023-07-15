import re

from rest_framework import serializers


def validate_username(value):
    if value == "me" or not re.match(r"^[\w.@+-]+\Z", value):
        raise serializers.ValidationError('Недопустимое имя пользователя!')
    return value
