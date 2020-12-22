from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, \
    SetPasswordForm, PasswordResetForm

from base_stuff_system.models import ExtendedUser
from django import forms
from django.contrib.auth.models import User
from .validators import unique_username, unique_email


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(self.fields[field].widget.attrs.update({'class': 'form-control'}))
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['username'].validators = [unique_username]
        self.fields['email'].validators = [unique_email]


class ExtendedProfileInfoForm(forms.ModelForm):
    class Meta:
        model = ExtendedUser
        fields = ('image', 'date_of_birth')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            (self.fields[field].widget.attrs.update({'class': 'form-control'}))
        self.fields['date_of_birth'].input_formats = ['%d/%m/%Y']


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            (self.fields[field].widget.attrs.update({'class': 'form-control'}))


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            (self.fields[field].widget.attrs.update({'class': 'form-control'}))


class CustomPasswordReset(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class CustomResetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
