from django.db import models


# Create your models here.


class BaseSchoolUser(models.Model):
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=25)
    age = models.PositiveIntegerField()
    user_type = models.CharField(max_length=10, choices=((1, 'teacher'), (2, 'student')), default='student')
    image = models.ImageField()


class Classroom(models.Model):
    title = models.CharField(max_length=20)
    student = models.ForeignKey(BaseSchoolUser, on_delete=models.CASCADE)


class Subject(models.Model):
    subject_name = models.CharField(max_length=20)
    student = models.ForeignKey(BaseSchoolUser, on_delete=models.CASCADE)


class Mark(models.Model):
    mark = models.PositiveIntegerField()
    date = models.DateTimeField()
    description = models.TextField(max_length=300)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class BehavioralAssessment(models.Model):
    title = models.CharField(max_length=20)
    date = models.DateTimeField()
    description = models.TextField(max_length=300)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(BaseSchoolUser, on_delete=models.CASCADE)
