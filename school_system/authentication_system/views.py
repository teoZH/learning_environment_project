from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SignUpForm, ExtendedProfileInfoForm, LoginForm, CustomPasswordChangeForm


# Create your views here.


def login_user(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('homepage')
        else:
            error = 'Wrong credentials. Try again!'
            print(error)
    else:
        form = LoginForm()
    return render(request, 'login_form.html', {'login_form': form, 'error': error})


@transaction.atomic
def register_user(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        extended_form = ExtendedProfileInfoForm(request.POST, request.FILES)
        if user_form.is_valid() and extended_form.is_valid():
            user = user_form.save()
            extend_info = extended_form.save(commit=False)
            extend_info.user = user
            extend_info.save()
            return redirect('login_user')
    else:
        user_form = SignUpForm()
        extended_form = ExtendedProfileInfoForm()

    context = {
        'user_form': user_form,
        'extended_form': extended_form
    }

    return render(request, 'register_form.html', context)


def change_password(request, user_id, username):
    user = get_object_or_404(User, pk=user_id, username=username)
    valid = user.username == request.user.username and user.pk == request.user.pk
    if not valid:
        return render(request,'access/not_authorized.html')
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user,request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'change_password.html', context)


def logout_user(request):
    logout(request)
    return redirect('homepage')
