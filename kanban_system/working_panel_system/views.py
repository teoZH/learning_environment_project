from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from base_stuff_system.models import ExtendedUser


def my_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    add_info = ExtendedUser.objects.get(user=user)
    return render(request, 'user_profile.html', {'user_info':user,
                                                 'additional':add_info})
