from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import ExtendBaseUser


# Create your views here.
def index(request):
    return render(request, 'base.html')


def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    add_info = ExtendBaseUser.objects.get(user=user)
    if add_info.user_type == 'teacher':
        return render(request, 'teacher_profile.html', {
            'user_info': user,
            'additional': add_info
    })

    return render(request,'profile/profile_page.html',{
            'user_info': user,
            'additional': add_info
    })
