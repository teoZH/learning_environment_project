from base_stuff_system.models import Company, Todo, Notes
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import ObjectDoesNotExist



class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'description', 'company')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['company'].required = False
        self.fields['company'].empty_label = 'myself'


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('title', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['description'].widget.attrs.update({"rows": "5"})


class EditProfileInfo(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserCharField(forms.CharField):

    def __init__(self, model_company=None, model_user=None, request_user=None, **kwargs):
        super().__init__(**kwargs)
        self.model_company = model_company
        self.model_user = model_user
        self.request_user = request_user

    def validate(self, value):
        if value in self.empty_values and self.required:
            raise ValidationError(self.error_messages['required'], code='required')

        if self.model_company:
            queryset = self.model_company.employee.filter(username=value)
            if queryset:
                raise ValidationError('The user is already added!')

        if self.model_user and self.request_user:
            try:
                user = self.model_user.objects.get(username=value)
                if user == self.request_user:
                    raise ValidationError("You cannot add yourself!")
            except ObjectDoesNotExist:
                raise ValidationError('Invalid username! Please try again!')


class AddUserForm(forms.Form):
    username = UserCharField(required=True, max_length=20, label='Type a valid username',
                             label_suffix='!')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields['username'].widget.attrs.update({"class": "form-control"})
