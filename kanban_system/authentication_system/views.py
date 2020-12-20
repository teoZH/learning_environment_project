from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode

from .forms import SignUpForm, ExtendedProfileInfoForm, LoginForm, CustomPasswordChangeForm, \
    CustomPasswordReset, CustomResetForm


# Create your views here.


def login_user(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('profile_page', user.pk)
        else:
            error = 'Wrong credentials. Try again!'
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
        return render(request, 'access/not_authorized.html')
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'change_password.html', context)


def reset_password(request):
    if request.method == 'POST':
        form = CustomPasswordReset(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            user = get_object_or_404(User, email=data)
            form.save(subject_template_name='pass_reset.txt', email_template_name='instructions.txt', request=request)
            return render(request,'see_email.html')
    form = CustomPasswordReset()
    return render(request, 'reset_password.html', {'form': form})


def set_password(request, uidb64, token):
    token_generator = default_token_generator
    user_id = int(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, pk=user_id)
    if token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomResetForm(user, request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'success_page.html')
        else:
            form = CustomResetForm(user)
        return render(request, 'set_new_password.html', {"form": form})
    else:
        return render(request, 'access/not_authorized.html')


def logout_user(request):
    logout(request)
    return redirect('not_registered')

# Create your views here.
