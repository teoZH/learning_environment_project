from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from basestuff.models import ExtendBaseUser
from django import forms
from django.contrib.auth.models import User


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


class ExtendedProfileInfoForm(forms.ModelForm):
    class Meta:
        model = ExtendBaseUser
        fields = ('user_type', 'image', 'age')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            (self.fields[field].widget.attrs.update({'class': 'form-control'}))


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
