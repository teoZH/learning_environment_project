from django.contrib import admin
from .models import Classroom, ExtendBaseUser, BehavioralAssessment, Subject, Mark

admin.site.register(Classroom)
admin.site.register(ExtendBaseUser)
admin.site.register(Subject)
admin.site.register(Mark)
admin.site.register(BehavioralAssessment)
