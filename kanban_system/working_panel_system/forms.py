from base_stuff_system.models import Company, Todo, Notes
from django import forms
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.forms.models import ModelChoiceField


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('title', 'user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


def create_choicesPersonalCompany(user_id):
    user = User.objects.get(pk=user_id)
    return [(user_id, (str(user)))]


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        exclude = ('user','in_progress','is_done')

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