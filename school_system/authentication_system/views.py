from django.contrib.auth import logout, authenticate, login
from django.db import transaction
from django.shortcuts import render, redirect

from .forms import SignUpForm, ExtendedProfileInfoForm, LoginForm


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


def logout_user(request):
    logout(request)
    return redirect('homepage')
