from django.contrib import admin
from .models import Classroom, BaseSchoolUser, BehavioralAssessment, Subject, Mark

admin.site.register(Classroom)
admin.site.register(BaseSchoolUser)
admin.site.register(Subject)
admin.site.register(Mark)
admin.site.register(BehavioralAssessment)
