from basestuff.models import Classroom, Subject, Mark, BehavioralAssessment
from django import forms


class CreateClassroom(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'


class CreateSubject(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'


class CreateMark(forms.ModelForm):
    class Meta:
        model = Mark
        fields = '__all__'


class CreateBehavioralAssessment(forms.ModelForm):
    class Meta:
        model = BehavioralAssessment
        fields = '__all__'
