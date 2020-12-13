from base_stuff_system.models import Company, Todo, Notes
from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('title','user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].disabled = True


def create_choicesPersonalCompany(user_id):
    return (User.objects.get(pk=user_id), 'myself'),


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].required = False
        self.fields['user'].empty_label = 'myself'
        self.fields['company'].required = False
        self.fields['company'].empty_label = 'myself'


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
