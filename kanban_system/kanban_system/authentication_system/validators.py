from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist
from django.core.exceptions import ValidationError


def unique_username(value):
    try:
        user = User.objects.get(username=value)
        raise ValidationError('Username already exists!')
    except ObjectDoesNotExist:
        pass


def unique_email(value):
    try:
        user = User.objects.get(email=value)
        raise ValidationError('Email already exists!')
    except ObjectDoesNotExist:
        pass