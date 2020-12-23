from base_stuff_system.models import Company, Todo, Notes
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import ObjectDoesNotExist
from django.forms import ModelChoiceField


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


class CustomModelChoiceField(ModelChoiceField):

    def __init__(self, todo=None, **kwargs):
        super().__init__(todo, **kwargs)
        self.__todo = todo

    @property
    def todo(self):
        return self.__todo

    @todo.setter
    def todo(self, new_todo: Todo):
        self.__todo = new_todo
        self.queryset = self.__todo.company.employee.all()

    def validate(self, value):
        if value in self.empty_values and self.required:
            raise ValidationError(self.error_messages['required'], code='required')
        if self.todo:
            print(value)
            if self.todo.user == value:
                raise ValidationError('You already assigned this user!')


class AddUserToTODO(forms.Form):
    add_user = CustomModelChoiceField(label='Select an user', label_suffix=':', required=True)
    todo_number = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['add_user'].widget.attrs.update({'class': 'form-control'})


def return_form_populated(form_class, todo_object, request=None):
    form = None

    if todo_object.company:
        if request is None:
            form = form_class()
        else:
            form = form_class(request.POST)
        form.fields['add_user'].todo = todo_object
        if len(form.fields['add_user'].queryset) == 0:
            print('asd')
            todo_object.form_error = True
        else:
            print('fake')
            todo_object.form_error = False
        form.fields['todo_number'].widget.attrs.update({"value": todo_object.pk})
    return form


def return_position_form(lst, todo):
    for x in range(len(lst)):
        if lst[x][0] == todo:
            return x
