from django.db.models import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.models import User
from base_stuff_system.models import Company
from django.core.exceptions import ValidationError


def check_for_object_availability(some_id, model):
    try:
        some = model.objects.get(pk=some_id)
    except ObjectDoesNotExist:
        return None
    return some


def check_correct_user(func):
    def wrapper(*args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['user_id'])
            if args[0].user != user:
                return render(args[0], 'access/not_authorized.html')
        except ObjectDoesNotExist:
            return render(args[0], 'access/not_authorized.html')
        return func(*args, **kwargs)

    return wrapper


def unique_title_check(value):
    try:
        company = Company.objects.get(title=value)

    except ObjectDoesNotExist:
        pass

